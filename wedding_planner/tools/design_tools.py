from langchain.tools import tool
from wedding_planner.tools.search import tavily_search
import logging

log = logging.getLogger(__name__)


@tool
def color_palette(style: str, season: str) -> str:
    """Generate color palette recommendations based on wedding style and season."""
    log.info(f"DesignAgent: generating color palette for {style} wedding in {season}")
    return tavily_search(f"wedding color palette {style} style {season} season trending colors combinations 2025 2026")


@tool
def floral_search(style: str, budget: str, season: str) -> str:
    """Search for floral arrangement ideas and pricing based on style, budget, and season."""
    log.info(f"DesignAgent: searching florals, style={style}, budget={budget}, season={season}")
    return tavily_search(f"wedding floral arrangements {style} style {budget} budget {season} seasonal flowers centerpieces bouquet")


@tool
def decor_inspiration(theme: str, budget: str) -> str:
    """Find décor inspiration and ideas for a given wedding theme and budget."""
    log.info(f"DesignAgent: finding décor inspiration for {theme} theme, budget={budget}")
    return tavily_search(f"wedding décor inspiration {theme} theme {budget} budget ideas reception ceremony decorations")
