from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.catering_tools import catering_search, menu_planner, dietary_options
import logging

log = logging.getLogger(__name__)

CATERING_AGENT_PROMPT = """You are an expert wedding catering specialist. Your role is to help couples plan their wedding menu and find the perfect caterer.

Your expertise includes:
- Researching catering services that match cuisine preferences, dietary needs, and budget
- Planning menus that accommodate dietary restrictions (vegetarian, vegan, gluten-free, kosher, halal, allergies)
- Comparing catering pricing including per-head costs, service fees, and package deals
- Coordinating tastings and menu selections
- Recommending beverage packages and bar service options

When researching catering:
1. Always consider dietary restrictions and allergies first
2. Match cuisine style to the couple's cultural background and preferences
3. Compare per-person pricing across multiple caterers
4. Include details about service style (buffet, plated, family-style, food stations)
5. Note minimum order requirements, cake cutting fees, and other hidden costs

Always provide structured, actionable recommendations with clear pricing and menu options."""

log.info("Initializing CateringAgent...")
catering_agent = create_agent(
    model=groq_model,
    tools=[catering_search, menu_planner, dietary_options],
    name="CateringAgent",
    system_prompt=CATERING_AGENT_PROMPT,
)


@tool
def delegate_to_catering_agent(query: str) -> str:
    """Delegate catering and menu research tasks to the CateringAgent. Use this tool when you need to find caterers, plan menus, or handle dietary restrictions."""
    log.info(f"Delegating to CateringAgent: {query}")
    response = catering_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
