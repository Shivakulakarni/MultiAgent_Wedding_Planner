from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def photographer_search(location: str, style: str, budget: str) -> str:
    """Search for wedding photographers matching style and budget in a given location."""
    log.info(f"PhotographyAgent: searching photographers in {location}, style={style}, budget={budget}")
    return tavily_search(f"best wedding photographers {location} {style} style {budget} budget packages 2025 2026")


@tool
def portfolio_review(photographer_name: str, location: str) -> str:
    """Review a photographer's portfolio, style, and past wedding work."""
    log.info(f"PhotographyAgent: reviewing portfolio for {photographer_name} in {location}")
    return tavily_search(f"{photographer_name} wedding photographer {location} portfolio samples reviews")


@tool
def photography_packages(photographer_name: str, location: str) -> str:
    """Get detailed photography package options, pricing, and what is included."""
    log.info(f"PhotographyAgent: getting packages for {photographer_name} in {location}")
    return tavily_search(f"{photographer_name} wedding photography packages pricing hours prints album engagement")
