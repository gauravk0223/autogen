from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.http import HttpTool

from dotenv import load_dotenv
import asyncio
import os
load_dotenv()

## Load OPENAI API KEY
api_key=os.getenv("OPENAI_API_KEY")

# Create model client 
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


'''
{
  "fact": "Normal body temperature for a cat is 102 degrees F.",
  "length": 51
}
'''
schema = {
    "type": "object",
    "properties": {
        "fact": {
            "type": "string",
            "description": "A trivia fact or statement."
        },
        "length": {
            "type": "integer",
            "description": "The length (number of characters) of the fact."
        }
    },
    "required": ["fact", "length"]
}

# Create an HTTP tool for the httpbin API
http_tool = HttpTool(
    name="cat_facts_api",
    description="get a cool cat fact",
    scheme="https",
    host="catfact.ninja",
    port=443,
    path="/fact",
    method="GET",
    return_type="json",
    json_schema=schema,
)


## Create an assistant Agent with model_client and tool, system message
assistant=AssistantAgent(
    name='CatFactsAgent',
    model_client=model_client,
    system_message="You are a assistant which can get some cool cats facts using the cat facts api tool.",
    tools=[http_tool],
    reflect_on_tool_use=True
)

async def main():
    result = await assistant.run(task="Fetch some facts around cats")
    ##print(result)
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())