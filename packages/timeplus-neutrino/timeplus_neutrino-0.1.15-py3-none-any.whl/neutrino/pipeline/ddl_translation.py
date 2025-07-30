from autogen_core import (
    AgentRuntime,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    message_handler,
    type_subscription,
    AgentId,
)
from autogen_core.models import (
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
)


from ..message import Message, AgentLogEvent

from ..conf import TimeplusAgentConfig
from ..logging import get_event_logger


logger = get_event_logger()


def get_instructions(db_type: str) -> str:
    return f"""You are an assistant rewrite DDL from timeplus to {db_type}.
NOTE :
1. Table name should be from the SETTINGS fields (database, table) instead of the external stream name
2. Only output the DDL using a sql markdown block

here is the timeplus stream DDL:
"""


ddl_translation_topic = "DDLTranslator"


@type_subscription(topic_type=ddl_translation_topic)
class DDLTranslator(RoutedAgent):
    def __init__(
        self,
        description: str,
        instructions: str,
        model_client: ChatCompletionClient,
    ) -> None:
        super().__init__(description=description)
        self._instructions = instructions
        self._system_message = SystemMessage(content=instructions)
        self._model_client = model_client

        self._result = None

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"{message.content}"
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        log_event = AgentLogEvent(
            agent_description=self._description,
            sender_topic=ddl_translation_topic,
            receiver_topic=ddl_translation_topic,
            system_message=self._system_message.content,
            user_prompt=prompt,
            response=response,
            model=str(self._model_client.model_info),
        )
        logger.info(log_event)
        self._result = response


async def _translate_ddl(
    runtime: AgentRuntime,
    model_client: ChatCompletionClient,
    ddl: str,
    db_type: str,
) -> None:
    await DDLTranslator.register(
        runtime,
        ddl_translation_topic,
        lambda: DDLTranslator(
            description="translate timeplus ddl to {db_type} ddl".format(
                db_type=db_type
            ),
            instructions=get_instructions(db_type),
            model_client=model_client,
        ),
    )

    message = f"""based on following input DDL : {ddl}"""

    runtime.start()

    await runtime.publish_message(
        Message(content=message),
        topic_id=TopicId(ddl_translation_topic, source="default"),
    )

    await runtime.stop_when_idle()

    agent_id = AgentId(ddl_translation_topic, "default")
    agent = await runtime.try_get_underlying_agent_instance(agent_id)

    translation_result = agent._result if agent and hasattr(agent, "_result") else None
    return translation_result


async def translate_ddl(
    ddl: str,
    db_type: str,
) -> None:
    agent_config = TimeplusAgentConfig()
    model_client = agent_config.get_client("default")

    runtime = SingleThreadedAgentRuntime()
    return await _translate_ddl(
        runtime=runtime, model_client=model_client, ddl=ddl, db_type=db_type
    )


def translate_ddl_sync(
    ddl: str,
    db_type: str,
) -> None:
    import asyncio

    return asyncio.run(translate_ddl(ddl, db_type))
