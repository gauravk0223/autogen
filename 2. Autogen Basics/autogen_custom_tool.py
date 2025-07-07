from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
from dotenv import load_dotenv
import os

## Load enviornmrnt variables
load_dotenv()

## Load OPENAI API KEY
api_key=os.getenv("OPENAI_API_KEY")

## Create brain/model_client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

## Create Custom functions to be used as Tool

def reverse_string(input : str ) -> str :
    """
    Tool to reverse the input string

    input: str 
    output: str

    """
    return input[::-1]

## Convert the def into tool using Function tool
reverse_tool = FunctionTool(reverse_string, description="Tool to reverse the input string")

## Create an assistant Agent with model_client and tool, system message
assistant = AssistantAgent(
    name='Assistant',
    model_client=model_client,
    system_message='You are a helpful assistant that can reverse string using reverse_string tool. Give the result with summary',
    tools=[reverse_tool],
    reflect_on_tool_use=True,
) 

async def main():
    
    print("In main")

    result = await assistant.run(task="Reverse the folloung string: Hi, My name is Gaurav")
    print(result)

if __name__ == "__main__":
    print("Main Module")
    asyncio.run(main())

