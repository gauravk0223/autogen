from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.http import HttpTool

from langchain_community.utilities import GoogleSerperAPIWrapper 

from dotenv import load_dotenv
import asyncio
import os
load_dotenv()

## Load OPENAI API KEY
api_key=os.getenv("OPENAI_API_KEY")

# Create model client 
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


os.environ['SERPER_API_KEY']='03efe53bf8044f01c84e9c0d43a252fc74dc64a7'

search_tool_wrapper = GoogleSerperAPIWrapper(type='news')


def search_web(query: str) -> str :
    """Search the web for thr given query and return the results."""
    try:
        results = search_tool_wrapper.run(query)
        return results
    except Exception as e :
        print(f"Error occurred while searching the web: {e}")
        return "No results found."  



## Create an assistant Agent with model_client and tool, system message
search_agent=AssistantAgent(
    name='searchAgent',
    model_client=model_client,
    system_message="You are a helpful assistant that can search the web for information using the search_web tool." \
    "Please make sure that you use the search_web tool to find information before you return the answer.",
    reflect_on_tool_use=True,
    tools=[search_web],

)

async def run_serper_search():
    """Run the search agent """
    query="Who won the IPL in 2025?"
    result = await search_agent.run(task=query)
    
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(run_serper_search())