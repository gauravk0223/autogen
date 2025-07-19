from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
import asyncio
from dotenv import load_dotenv
import os

## Load enviornmrnt variables
load_dotenv()

## Load OPENAI API KEY
api_key=os.getenv("OPENAI_API_KEY")

## Create brain/model_client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

assitant = AssistantAgent(
    name='AI_Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who help on the task given',
)

user_proxy_agent = UserProxyAgent(
    name='userproxy',
    description='',
    input_func=input
)

termination_condition=TextMentionTermination(text='APPROVE')

team = RoundRobinGroupChat(
    participants=[assitant, user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=10
)


stream = team.run_stream(task = 'Write a great poem about india in 100 words?')

async def main():
    await Console(stream)

if (__name__ == '__main__'):
    asyncio.run(main())