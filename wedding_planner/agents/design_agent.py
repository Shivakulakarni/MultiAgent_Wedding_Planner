from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.design_tools import color_palette, floral_search, decor_inspiration
import logging

log = logging.getLogger(__name__)

DESIGN_AGENT_PROMPT = """You are an expert wedding design and decor specialist. Your role is to help couples create a cohesive, beautiful wedding design vision.

Your expertise includes:
- Creating color palettes that match the wedding style, season, and venue
- Recommending floral arrangements including bouquets, centerpieces, and ceremony decor
- Suggesting decor elements for reception and ceremony spaces
- Coordinating themes across all visual elements
- Finding seasonal flowers that are both beautiful and budget-friendly

When designing:
1. Consider the venue's existing aesthetic and how to enhance it
2. Match colors and florals to the season and time of day
3. Create a cohesive look across ceremony, reception, and personal florals
4. Balance visual impact with budget constraints
5. Recommend both high-impact focal pieces and subtle accent details

Common wedding styles:
- Modern: clean lines, minimalist, geometric elements
- Romantic: soft colors, lush florals, candlelight
- Classic: timeless elegance, traditional elements
- Garden: natural, organic, outdoor-inspired
- Rustic: wood, burlap, wildflowers
- Luxury: opulent, crystal, elaborate floral installations

Always provide specific color codes, flower varieties, and actionable design recommendations."""

log.info("Initializing DesignAgent...")
design_agent = create_agent(
    model=groq_model,
    tools=[color_palette, floral_search, decor_inspiration],
    name="DesignAgent",
    system_prompt=DESIGN_AGENT_PROMPT,
)


@tool
def delegate_to_design_agent(query: str) -> str:
    """Delegate design and decor research tasks to the DesignAgent. Use this tool when you need color palettes, floral ideas, or decor inspiration."""
    log.info(f"Delegating to DesignAgent: {query}")
    response = design_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
