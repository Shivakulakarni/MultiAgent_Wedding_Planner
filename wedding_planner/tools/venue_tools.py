from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def venue_search(location: str, budget: str, capacity: int, style: str) -> str:
    """Search for wedding venues matching location, budget, guest capacity, and style preferences."""
    log.info(f"VenueAgent: searching venues in {location} for {capacity} guests, style={style}, budget={budget}")
    return tavily_search(f"best wedding venues {location} {capacity} guests {style} style {budget} budget 2025 2026")


@tool
def venue_pricing(venue_name: str, location: str) -> str:
    """Get detailed pricing information for a specific wedding venue."""
    log.info(f"VenueAgent: getting pricing for {venue_name} in {location}")
    return tavily_search(f"{venue_name} wedding venue {location} pricing cost rental fee per person")


@tool
def venue_reviews(venue_name: str, location: str) -> str:
    """Get reviews and ratings for a specific wedding venue."""
    log.info(f"VenueAgent: getting reviews for {venue_name} in {location}")
    return tavily_search(f"{venue_name} wedding venue {location} reviews ratings testimonials")
