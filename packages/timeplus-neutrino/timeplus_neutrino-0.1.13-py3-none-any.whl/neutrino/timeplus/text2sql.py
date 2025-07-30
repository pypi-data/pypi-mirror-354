import re
import asyncio

from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

from ..mcp.mcp_server import list_databases, list_tables

from ..conf import TimeplusAgentConfig


# NOTE: this ReAct prompt is adapted from Langchain's ReAct agent: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/agents/react/agent.py#L79
ReAct_system_prompt = """You are a asistent help generating SQL based on input questions.
Please stop when you have the SQL, no need to execute the SQL
To generate SQL, here are rules:
* the grammar follows ClickHouse style
* all datatypes MUST be in lowercase, such uint32
* all keywords MUST be in lowercase, such as nullable
* for normal query, add table() function to the table name, for example select count(*) from table(table_name)
* for real time query, where continously return new result to the user, append a time range, for example
  select count(*) from table_name where _tp_time > now() -1h
  which will return the number of event received in the past 1 hour

You have access to tools provided.
including
1. list_databases() which returns the list of all databases
2. list_tables(database:str) which returns details of all tables in the given database

Once the SQL is generate, terminate the chat and provide the SQL as Final Answer

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Action Input: the input to the action
Observation: the result of the action
... (this process can repeat multiple times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Question: {input}
"""


def extract_final_answer(llm_response):
    # Pattern to match "Final answer:" (case insensitive) and capture everything after it
    pattern = r"Final [Aa]nswer:\s*(.*?)(?:\n\n|$)"

    # Use re.DOTALL flag to make the dot match newlines as well
    # This will capture multi-line final answers
    match = re.search(pattern, llm_response, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return None


class Text2SQLAgent:
    def __init__(self):
        self.agent_config = TimeplusAgentConfig()
        config = self.agent_config._get_config("default")
        self.model_client = OpenAIChatCompletionClient(
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
            temperature=0.0,
        )

        self.agent = AssistantAgent(
            name="assistant",
            model_client=self.model_client,
            tools=[list_databases, list_tables],
            system_message=ReAct_system_prompt,
            reflect_on_tool_use=False,
        )

    async def ask_async(self, question: str):
        source = "user"
        count = 0
        response = None
        input = question
        while True:
            if "final answer" in input.lower():
                print(f"Found 'Final answer' {input} (case-insensitive)!")
                break

            response = await self.agent.on_messages(
                [TextMessage(content=question, source=source)], CancellationToken()
            )
            input = response.chat_message.content
            source = "Assistant"
            count += 1
            if count > 20:
                print("Max iteration reached, exit")
                break

        return extract_final_answer(response.chat_message.content)

    def ask(self, question: str):
        """Synchronous wrapper for ask_async method"""
        return asyncio.run(self.ask_async(question))
