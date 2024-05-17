from langchain.tools import BaseTool
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
import requests

class PrometheusQueryToolConfig(BaseModel):
    prometheus_url: str = Field(default="http://localhost:9090")

class PrometheusQueryTool(BaseTool):
    name = "Prometheus Query"
    description = "Tool for querying a Prometheus server"
    config: Optional[PrometheusQueryToolConfig] = None

    def __init__(self, prometheus_url: str = "http://localhost:9090"):
        super().__init__()
        self.config = PrometheusQueryToolConfig(prometheus_url=prometheus_url)

    def _run(self, query: str):
        params = {'query': query}
        response = requests.get(f"{self.config.prometheus_url}/api/v1/query", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.text}"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

# Initialize the Prometheus Query Tool with the URL of your Prometheus server
prometheus_tool = PrometheusQueryTool(prometheus_url="http://localhost:9090")


# Initialize LLM (ChatOpenAI)
llm = ChatOpenAI(temperature=0, model_name='gpt-4')

# Include the Prometheus tool in the list of tools
tools = [prometheus_tool]

# Prompt for the agent
prompt = """
Use metrics to answer this question:
{text}
"""

# Initialize agent with tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=True,
)

# Example query to the agent
response = agent(prompt.format(text="Can you give the increase in count of running pods from since past 2 mins, calculate the count step by step?"))
print(response)
