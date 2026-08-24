from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.venue_tools import venue_search, venue_pricing, venue_reviews
import logging

log = logging.getLogger(__name__)

VENUE_AGENT_PROMPT = """You are an expert wedding venue specialist. Your role is to help couples find the perfect wedding venue.

Your expertise includes:
- Researching venues that match the couple's capacity, style, budget, and location preferences
- Comparing pricing across multiple venues including rental fees, per-person costs, and hidden fees
- Analyzing venue reviews and ratings from past couples
- Evaluating venue amenities, accessibility, parking, and accommodation options
- Assessing venue availability and booking timelines

When researching venues:
1. Always consider the guest count, budget, and preferred style
2. Compare at least 3-5 venues when possible
3. Include pricing details, capacity, and key features
4. Note any restrictions or requirements (minimum spend, vendor lists, etc.)
5. Highlight unique features that match the couple's vision

Always provide structured, actionable recommendations with clear rationale."""

log.info("Initializing VenueAgent...")
venue_agent = create_agent(
    model=groq_model,
    tools=[venue_search, venue_pricing, venue_reviews],
    name="VenueAgent",
    system_prompt=VENUE_AGENT_PROMPT,
)


@tool
def delegate_to_venue_agent(query: str) -> str:
    """Delegate venue research tasks to the VenueAgent. Use this tool when you need to find, compare, or analyze wedding venues including pricing, availability, reviews, and features."""
    log.info(f"Delegating to VenueAgent: {query}")
    response = venue_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
