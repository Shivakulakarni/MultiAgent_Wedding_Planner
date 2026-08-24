from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.guest_tools import rsvp_tracker, seating_chart, dietary_manager
import logging

log = logging.getLogger(__name__)

GUEST_AGENT_PROMPT = """You are an expert wedding guest management specialist. Your role is to help couples manage their guest list, RSVPs, seating, and dietary needs.

Your expertise includes:
- Creating and managing guest lists with RSVP tracking
- Designing seating charts that maximize guest experience
- Handling dietary restrictions and special requirements
- Managing plus-ones, children, and VIP guests
- Coordinating welcome bags and guest favors

When managing guests:
1. Create a structured guest list with categories (family, friends, colleagues, VIPs)
2. Design seating charts that consider relationships, dynamics, and dietary needs
3. Track RSVPs and follow up with non-respondents
4. Accommodate dietary restrictions including allergies, vegetarian, vegan, kosher, halal
5. Plan guest experience from arrival through farewell

Guest management checklist:
- Build initial guest list with priorities
- Send save-the-dates and track responses
- Manage RSVPs and dietary requirements
- Create seating chart based on relationships and needs
- Plan welcome bags for out-of-town guests
- Coordinate day-of guest experience

Always provide specific, actionable recommendations for guest management."""

log.info("Initializing GuestAgent...")
guest_agent = create_agent(
    model=groq_model,
    tools=[rsvp_tracker, seating_chart, dietary_manager],
    name="GuestAgent",
    system_prompt=GUEST_AGENT_PROMPT,
)


@tool
def delegate_to_guest_agent(query: str) -> str:
    """Delegate guest management tasks to the GuestAgent. Use this tool when you need RSVP tracking, seating charts, or dietary management."""
    log.info(f"Delegating to GuestAgent: {query}")
    response = guest_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
