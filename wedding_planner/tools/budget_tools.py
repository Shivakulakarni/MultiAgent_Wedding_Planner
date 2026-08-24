from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def budget_breakdown(total_budget: int, guest_count: int, location: str) -> str:
    """Calculate optimal budget allocation across wedding categories (venue, catering, photography, flowers, music, attire, etc.)."""
    log.info(f"BudgetAgent: calculating breakdown for ${total_budget}, {guest_count} guests, {location}")
    return tavily_search(f"wedding budget breakdown allocation percentage {total_budget} total {guest_count} guests {location} average costs 2025 2026")


@tool
def cost_comparison(category: str, location: str, budget_range: str) -> str:
    """Compare costs for a specific wedding category to find best value options."""
    log.info(f"BudgetAgent: comparing costs for {category} in {location}, budget={budget_range}")
    return tavily_search(f"wedding {category} cost comparison {location} {budget_range} budget average price range")


@tool
def savings_tips(wedding_style: str, total_budget: int) -> str:
    """Find cost-saving tips and strategies for weddings while maintaining quality."""
    log.info(f"BudgetAgent: finding savings tips for {wedding_style} wedding, budget=${total_budget}")
    return tavily_search(f"wedding budget saving tips {wedding_style} style save money without sacrificing quality 2025 2026")
