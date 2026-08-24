from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def rsvp_tracker(guest_count: int, wedding_style: str) -> str:
    """Get tips and tools for tracking RSVPs, managing responses, and following up with guests."""
    log.info(f"GuestAgent: researching RSVP tracking for {guest_count} guests, style={wedding_style}")
    return tavily_search(f"wedding RSVP tracking tips tools manage responses {guest_count} guests follow up strategies")


@tool
def seating_chart(guest_count: int, venue_type: str) -> str:
    """Get seating chart strategies, layout ideas, and tips for arranging guests."""
    log.info(f"GuestAgent: researching seating for {guest_count} guests, venue={venue_type}")
    return tavily_search(f"wedding seating chart strategies {guest_count} guests {venue_type} arrangement tips table layout")


@tool
def dietary_manager(dietary_restrictions: str) -> str:
    """Manage guest dietary requirements including allergies, vegetarian, vegan, kosher, and halal needs."""
    log.info(f"GuestAgent: managing dietary requirements: {dietary_restrictions}")
    return tavily_search(f"wedding guest dietary requirements management {dietary_restrictions} allergy accommodations caterer communication")
