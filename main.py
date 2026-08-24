from prompts import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT
from langchain.agents import create_agent
from models import groq_model
from agents import delegate_to_subagent1, delegate_to_subagent2
import logging
from langchain.messages import HumanMessage


# configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# asking user for their requirements for their wedding
logging.info("asking user for their requirements...")
user_requirements = input("Please enter your requirements and preferences for your wedding: ")


# updating the system prompt with the user's requirements
updated_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=user_requirements)


# creating main agent
logging.info("initializing Main wedding planner agent...")
main_wedding_planner_agent = create_agent(model=groq_model, 
                                          tools=[delegate_to_subagent1, delegate_to_subagent2], 
                                          name="MainWeddingPlannerAgent", 
                                          system_prompt=updated_system_prompt)


# invoking main agent
logging.info("invoking Main wedding planner agent...")
main_wedding_planner_agent_response = main_wedding_planner_agent.invoke({"messages":[HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]})

# printing the response from the main agent
print("\nMain Wedding Planner Agent's Response:")
print(main_wedding_planner_agent_response["messages"][-1].content)
