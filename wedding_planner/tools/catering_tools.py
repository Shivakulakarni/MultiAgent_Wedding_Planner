from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def catering_search(location: str, cuisine: str, budget: str, guest_count: int) -> str:
    """Search for wedding catering services matching cuisine, budget, and guest count."""
    log.info(f"CateringAgent: searching caterers in {location}, cuisine={cuisine}, budget={budget}, guests={guest_count}")
    return tavily_search(f"best wedding catering {location} {cuisine} cuisine {budget} budget {guest_count} guests per person price")


@tool
def menu_planner(cuisine: str, dietary_restrictions: str, budget_per_head: str) -> str:
    """Plan a wedding menu based on cuisine preference, dietary restrictions, and per-head budget."""
    log.info(f"CateringAgent: planning menu, cuisine={cuisine}, dietary={dietary_restrictions}, budget={budget_per_head}")
    return tavily_search(f"wedding menu planning {cuisine} cuisine {dietary_restrictions} dietary {budget_per_head} per person sample menu")


@tool
def dietary_options(restrictions: str) -> str:
    """Research dietary accommodation options for wedding catering including vegetarian, vegan, gluten-free, and allergy-friendly choices."""
    log.info(f"CateringAgent: researching dietary options for {restrictions}")
    return tavily_search(f"wedding catering dietary restrictions {restrictions} options menu ideas accommodate guests")
