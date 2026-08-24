from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.travel_tools import accommodation_search, transportation_planner, destination_research
import logging

log = logging.getLogger(__name__)

TRAVEL_AGENT_PROMPT = """You are an expert wedding travel and logistics specialist. Your role is to help couples manage guest travel, accommodations, and destination wedding logistics.

Your expertise includes:
- Finding hotel room blocks with group rates near the wedding venue
- Planning guest transportation including shuttles, parking, and ride-sharing
- Researching destination weddings including legal requirements and logistics
- Coordinating welcome bags, rehearsal dinner travel, and post-wedding brunch
- Managing out-of-town guest needs and recommendations

When planning travel:
1. Prioritize proximity to the venue and group rate availability
2. Consider different budget levels for guest accommodations
3. Plan transportation logistics for the wedding day
4. For destination weddings, research legal requirements and vendor availability
5. Create welcome packets with local recommendations and event schedules

Always provide specific hotel recommendations, pricing ranges, and logistical action items."""

log.info("Initializing TravelAgent...")
travel_agent = create_agent(
    model=groq_model,
    tools=[accommodation_search, transportation_planner, destination_research],
    name="TravelAgent",
    system_prompt=TRAVEL_AGENT_PROMPT,
)


@tool
def delegate_to_travel_agent(query: str) -> str:
    """Delegate travel and logistics research tasks to the TravelAgent. Use this tool when you need hotel accommodations, transportation planning, or destination research."""
    log.info(f"Delegating to TravelAgent: {query}")
    response = travel_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
