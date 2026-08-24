from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def accommodation_search(location: str, check_in: str, check_out: str, guest_count: int) -> str:
    """Search for hotel accommodations near the wedding venue for out-of-town guests."""
    log.info(f"TravelAgent: searching hotels in {location}, guests={guest_count}")
    return tavily_search(f"hotels near {location} wedding venue group rates {guest_count} rooms {check_in} to {check_out} block booking")


@tool
def transportation_planner(venue: str, guest_count: int, location: str) -> str:
    """Plan guest transportation including shuttles, parking, and ride-sharing options."""
    log.info(f"TravelAgent: planning transportation to {venue}, {guest_count} guests, {location}")
    return tavily_search(f"wedding guest transportation {venue} {location} shuttle service valet parking ride share coordination")


@tool
def destination_research(destination: str, guest_count: int, budget: str) -> str:
    """Research a wedding destination including logistics, requirements, and costs."""
    log.info(f"TravelAgent: researching destination {destination}, {guest_count} guests, budget={budget}")
    return tavily_search(f"destination wedding {destination} logistics requirements costs travel {guest_count} guests {budget} budget")
