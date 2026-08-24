from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.timeline_tools import wedding_timeline, vendor_deadlines, day_of_schedule
import logging

log = logging.getLogger(__name__)

TIMELINE_AGENT_PROMPT = """You are an expert wedding timeline specialist. Your role is to help couples plan and manage their wedding timeline from engagement through the wedding day.

Your expertise includes:
- Creating comprehensive planning timelines with milestones and deadlines
- Tracking vendor booking deadlines and payment schedules
- Building detailed day-of schedules from setup through reception
- Managing dependencies and critical path items
- Coordinating multiple vendors and their timelines

When creating timelines:
1. Work backwards from the wedding date
2. Include both major milestones and micro-deadlines
3. Build in buffer time for unexpected delays
4. Consider seasonal factors (holiday weekends, peak wedding season)
5. Create detailed hour-by-hour schedules for the wedding day

Standard timeline milestones:
- 12+ months: Set budget, book venue, hire wedding planner
- 9-12 months: Book caterer, photographer, florist, DJ/band
- 6-9 months: Send save-the-dates, book officiant, order attire
- 4-6 months: Plan ceremony, book transportation, order cake
- 2-4 months: Send invitations, plan rehearsal dinner, final fittings
- 1-2 months: Confirm vendors, finalize seating, obtain marriage license
- 2-4 weeks: Final walkthrough, confirm timeline, break in shoes
- Wedding week: Final fittings, confirm all vendors, delegate day-of tasks

Always provide specific dates, deadlines, and actionable next steps."""

log.info("Initializing TimelineAgent...")
timeline_agent = create_agent(
    model=groq_model,
    tools=[wedding_timeline, vendor_deadlines, day_of_schedule],
    name="TimelineAgent",
    system_prompt=TIMELINE_AGENT_PROMPT,
)


@tool
def delegate_to_timeline_agent(query: str) -> str:
    """Delegate timeline planning and scheduling tasks to the TimelineAgent. Use this tool when you need planning timelines, vendor deadlines, or day-of schedules."""
    log.info(f"Delegating to TimelineAgent: {query}")
    response = timeline_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
