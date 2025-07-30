import json
import re
from typing import Annotated, List

from autogen_core import (
    AgentRuntime,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    DefaultTopicId,
    message_handler,
    type_subscription,
    AgentId,
)
from autogen_core.models import (
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
    LLMMessage,
)
from autogen_core.model_context import (
    BufferedChatCompletionContext,
    ChatCompletionContext,
)

from autogen_core.tool_agent import ToolAgent, tool_agent_caller_loop
from autogen_core.tools import FunctionTool, Tool, ToolSchema

from ..message import Message, AgentLogEvent

from ..kafka.tools import explore_kafka_topic
from ..timeplus.utils import convert_confluent_to_stream_settings
from ..conf import TimeplusAgentConfig
from ..logging import get_event_logger

from ..onboard.agent import DataOnboardingAgent
from .agent import DataExtractionAgent

logger = get_event_logger()


def get_instructions() -> str:
    return """You are an assistant for building Debezium pipelines.

SIMPLE PROCESS:
1. call explore_kafka_topic() to get one sample event from the kafka topic
2. call infer_kafka_external_stream() to infer the Timeplus external stream DDL schema from the sample event,
   using the sample events as data input, using the kafka setting and topic name as external stream properties.
   should use raw format to infer the schema.
   generate other input parameters as needed, such as stream name, description, database.
3. call generate_extraction_mv_and_target_stream() to generate the extraction materialized view and target stream DDLs.
   using an emptry dictionary for settings if no settings are provided.

return the infered DDLs of source exteranl stream, target stream and extraction materialized view.

the output should be a json object with the following keys:
"topic": the Kafka topic name
"kafka_config": the kafka properties
"source_stream": the source external stream DDL
"target_stream": the target stream DDL
"extraction_mv": the extraction materialized view DDL

"""


cdc_pipeline_topic = "DebeziumPipelineBuilder"


@type_subscription(topic_type=cdc_pipeline_topic)
class DebeziumPipelineBuilder(RoutedAgent):
    def __init__(
        self,
        description: str,
        instructions: str,
        model_client: ChatCompletionClient,
        model_context: ChatCompletionContext,
        tool_schema: List[ToolSchema],
        tool_agent_type: str,
    ) -> None:
        super().__init__(description=description)
        self._instructions = instructions
        self._system_messages: List[LLMMessage] = [SystemMessage(content=instructions)]
        self._model_client = model_client
        self._tool_schema = tool_schema
        self._tool_agent_id = AgentId(tool_agent_type, self.id.key)
        self._model_context = model_context

        self._result = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:

        try:
            # Add the user message to the model context.
            await self._model_context.add_message(
                UserMessage(content=message.content, source=self.id.key)
            )

            # Run the caller loop to handle tool calls.
            messages = await tool_agent_caller_loop(
                self,
                tool_agent_id=self._tool_agent_id,
                model_client=self._model_client,
                input_messages=self._system_messages
                + (await self._model_context.get_messages()),
                tool_schema=self._tool_schema,
                cancellation_token=ctx.cancellation_token,
            )

            # Add the assistant message to the model context.
            for msg in messages:
                await self._model_context.add_message(msg)

            # Publish the final response.
            assert isinstance(messages[-1].content, str)
            response_message = Message(content=messages[-1].content)

            log_event = AgentLogEvent(
                agent_description=self._description,
                sender_topic=cdc_pipeline_topic,
                receiver_topic=cdc_pipeline_topic,
                system_message=self._instructions,
                user_prompt=message.content,
                response=response_message.content,
                model=str(self._model_client.model_info),
            )
            logger.info(log_event)

            self._result = response_message.content

            await self.publish_message(response_message, DefaultTopicId())

        except Exception as e:
            raise e


def infer_kafka_external_stream(
    data: Annotated[str, "sample of events from the Kafka topic"],
    topic: Annotated[str, "the Kafka topic name"],
    properties: Annotated[
        str,
        "a dictionary string of properties to use when creating the kafka external stream",
    ] = "{}",
    description: Annotated[str, "description of the stream"] = "",
    database: Annotated[
        str, "The name of the database to create the stream"
    ] = "default",
):
    """
    Infer a Timeplus external stream from a given Kafka topic.

    Given a sample of data from a Kafka topic, this function will return a SQL DDL
    statement that can be used to create an external stream in Timeplus.

    Args:
        data (str): sample of events from the Kafka topic.
        topic (str): The name of topic.
        properties (str): A dictionary string of properties to use when creating the stream.
        description (str, optional): A description of the stream. Defaults to "".
        database (str, optional): The name of the database to create the stream in. Defaults to "default".

    Returns:
        str: A SQL DDL statement that can be used to create the stream.
    """

    source_stream_name = f"{sanitize_table_name(topic)}_source_stream"
    agent = DataOnboardingAgent()
    inference_ddl, _ = agent.inference_external_stream(
        data,
        source_stream_name,
        properties,
        description,
        database=database,
        raw_format=True,
    )
    return inference_ddl


def sanitize_table_name(name: str) -> str:
    # Replace any character that is not a-z, A-Z, 0-9, or _ with _
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # Optionally, remove leading digits or underscores to match ClickHouse rules better
    sanitized = re.sub(r"^[^a-zA-Z]+", "", sanitized)
    return sanitized


def generate_extraction_mv_and_target_stream(
    sample_data: Annotated[str, "sample events from the Kafka topic"],
    topic: Annotated[str, "the Kafka topic name"],
    database: Annotated[str, "the database name"],
    settings: Annotated[str, "additional settings for the target stream"],
):
    """
    Generate pipeline resources DDLs from a sample Debezium CDC data and kafka topic.

    This function creates the necessary DDLs for setting up a pipeline to process
    Debezium CDC data. It generates an external source stream DDL, a target stream
    DDL, and an extraction materialized view DDL.

    Args:
        sample_data (str): A dictionary representing a sample of the Debezium CDC data payload.
        topic (str): The Kafka topic name associated with the data.
        database (str): The name of the database to create the stream in.
        settings (str): Additional settings or configurations for the target stream.
        - "type": The type of the stream (e.g., "append only stream", "mutable stream", "mysql external table", "s3 exteral table", "kafka external stream").


    Returns:
        dict: A dictionary containing:
            - "target_stream": The inferred target stream DDL as a string.
            - "extraction_mv": The inferred extraction materialized view DDL as a string.
    """

    source_stream_name = f"{sanitize_table_name(topic)}_source_stream"
    target_stream_name = f"{sanitize_table_name(topic)}_target_stream"

    settings_obj = json.loads(settings) if settings else {}

    agent = DataExtractionAgent()
    agent1_output, agent2_output = agent.generic_pipeline(
        sample_data,
        source_stream_name,
        target_stream_name,
        database,
        properties=settings_obj,
    )
    return {
        "target_stream": agent1_output,
        "extraction_mv": agent2_output,
    }


async def _build_debezium_pipeline(
    runtime: AgentRuntime,
    model_client: ChatCompletionClient,
    topic: str,
    kafka_config: dict,
    database: str = "default",
    target_stream_settings: dict = {}
) -> None:

    agent_tools: List[Tool] = [
        FunctionTool(
            explore_kafka_topic,
            name="explore_kafka_topic",
            description="explore a Kafka topic by consuming messages.",
        ),
        FunctionTool(
            infer_kafka_external_stream,
            name="infer_kafka_external_stream",
            description="infer the Timeplus external stream DDL schema from Kafka sample events.",
        ),
        FunctionTool(
            generate_extraction_mv_and_target_stream,
            name="generate_extraction_mv_and_target_stream",
            description="generate the extraction materialized view and target stream DDLs from Kafka sample events.",
        ),
    ]

    await ToolAgent.register(
        runtime,
        "ToolAgent",
        lambda: ToolAgent(
            description="Tool agent for pipeline builder.", tools=agent_tools
        ),
    )

    await DebeziumPipelineBuilder.register(
        runtime,
        cdc_pipeline_topic,
        lambda: DebeziumPipelineBuilder(
            description="build dezezium pipeline.",
            instructions=get_instructions(),
            model_client=model_client,
            model_context=BufferedChatCompletionContext(buffer_size=10),
            tool_schema=[tool.schema for tool in agent_tools],
            tool_agent_type="ToolAgent",
        ),
    )

    # TODO : support more additional settings
    additional_settings = {"topic": topic}

    external_stream_config = convert_confluent_to_stream_settings(
        kafka_config, **additional_settings
    )

    message = f"""based on following input
    kafka topic : {topic},
    kafka config : {json.dumps(kafka_config)},
    external stream properties : {json.dumps(external_stream_config)},
    timeplusd database : {database},
    target stream settings : {json.dumps(target_stream_settings)}
    build a debezium pipeline.
    """
    runtime.start()

    await runtime.publish_message(
        Message(content=message),
        topic_id=TopicId(cdc_pipeline_topic, source="default"),
    )

    await runtime.stop_when_idle()

    agent_id = AgentId(cdc_pipeline_topic, "default")
    agent = await runtime.try_get_underlying_agent_instance(agent_id)

    pipline_result = agent._result if agent and hasattr(agent, "_result") else None
    return pipline_result


async def build_debezium_pipeline(
    topic: str,
    kafka_config: dict,
    database: str = "default",
    target_stream_settings: dict = {},
) -> None:
    agent_config = TimeplusAgentConfig()
    model_client = agent_config.get_client("default")

    runtime = SingleThreadedAgentRuntime()
    return await _build_debezium_pipeline(
        runtime=runtime,
        model_client=model_client,
        topic=topic,
        kafka_config=kafka_config,
        database=database,
        target_stream_settings=target_stream_settings
    )


def build_debezium_pipeline_sync(
    topic: str,
    kafka_config: dict,
    database: str = "default",
    target_stream_settings: dict = {},
) -> None:
    """
    Synchronous wrapper for building a Debezium pipeline.

    Args:
        topic (str): The Kafka topic to build the pipeline for.
    """
    import asyncio

    return asyncio.run(
        build_debezium_pipeline(topic, kafka_config, database, target_stream_settings)
    )
