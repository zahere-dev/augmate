from agents.base_agent import Agent
from tools.weather_tool import WeatherTool
from tools.time_tool import TimeTool
from orchestrator import AgentOrchestrator

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Weather Agent
weather_agent = Agent(
    Name="Weather Agent",
    Description="Provides weather information for a given location",
    Tools=[WeatherTool()],
    Model="gpt-4o-mini"
)

# Create Time Agent
time_agent = Agent(
    Name="Time Agent",
    Description="Provides the current time for a given city",
    Tools=[TimeTool()],
    Model="gpt-4o-mini"
)

# Create AgentOrchestrator
agent_orchestrator = AgentOrchestrator([weather_agent, time_agent])

# Run the orchestrator
agent_orchestrator.run()

