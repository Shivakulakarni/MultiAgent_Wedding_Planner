from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
from datetime import datetime
import logging

log = logging.getLogger(__name__)


@tool
def wedding_timeline(wedding_date: str, guest_count: int, budget: str) -> str:
    """Generate a comprehensive wedding planning timeline from today until the wedding date."""
    log.info(f"TimelineAgent: generating timeline for wedding on {wedding_date}, {guest_count} guests")
    try:
        date_obj = datetime.strptime(wedding_date, "%Y-%m-%d")
        months_out = (date_obj - datetime.now()).days // 30
        days_until = (date_obj - datetime.now()).days
    except ValueError:
        months_out = 12
        days_until = "unknown"
    timeline_data = tavily_search(f"wedding planning timeline checklist {months_out} months out milestones deadlines tasks")
    return f"**Wedding Date:** {wedding_date} ({days_until} days away)\n\n**Planning Timeline:**\n\n{timeline_data}"


@tool
def vendor_deadlines(wedding_date: str, services: str) -> str:
    """Get recommended booking deadlines for wedding vendors and services."""
    log.info(f"TimelineAgent: getting vendor deadlines for {services}, wedding={wedding_date}")
    return tavily_search(f"wedding vendor booking deadlines timeline {services} when to book how far in advance")


@tool
def day_of_schedule(wedding_date: str, ceremony_time: str, reception_venue: str) -> str:
    """Create a detailed day-of wedding schedule including setup, ceremony, and reception timelines."""
    log.info(f"TimelineAgent: creating day-of schedule, ceremony={ceremony_time}, reception={reception_venue}")
    return tavily_search(f"wedding day of schedule timeline template ceremony {ceremony_time} reception schedule hour by hour")
