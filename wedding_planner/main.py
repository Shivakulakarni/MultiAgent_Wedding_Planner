from wedding_planner.prompts import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT
from wedding_planner.models import groq_model
from wedding_planner.agents import (
    delegate_to_venue_agent,
    delegate_to_catering_agent,
    delegate_to_photography_agent,
    delegate_to_budget_agent,
    delegate_to_design_agent,
    delegate_to_timeline_agent,
    delegate_to_travel_agent,
    delegate_to_guest_agent,
)
from langchain.agents import create_agent
from langchain.messages import HumanMessage
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

log.info("asking user for their requirements...")
user_requirements = input("Please enter your requirements and preferences for your wedding: ")

updated_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=user_requirements)

log.info("initializing Main wedding planner agent with 8 specialized agents...")
main_agent = create_agent(
    model=groq_model,
    tools=[
        delegate_to_venue_agent,
        delegate_to_catering_agent,
        delegate_to_photography_agent,
        delegate_to_budget_agent,
        delegate_to_design_agent,
        delegate_to_timeline_agent,
        delegate_to_travel_agent,
        delegate_to_guest_agent,
    ],
    name="MainWeddingPlannerAgent",
    system_prompt=updated_system_prompt,
)

log.info("invoking Main wedding planner agent...")
response = main_agent.invoke({"messages": [HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]})

print("\nMain Wedding Planner Agent's Response:")
print(response["messages"][-1].content)
