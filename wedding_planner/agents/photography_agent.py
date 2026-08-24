from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.photography_tools import photographer_search, portfolio_review, photography_packages
import logging

log = logging.getLogger(__name__)

PHOTOGRAPHY_AGENT_PROMPT = """You are an expert wedding photography specialist. Your role is to help couples find the perfect photographer to capture their wedding day.

Your expertise includes:
- Finding photographers that match the couple's style (candid, editorial, traditional, documentary, fine art)
- Comparing photography packages, pricing, and what is included
- Reviewing portfolios and past wedding work
- Understanding photography timelines for the wedding day
- Recommending engagement session and pre-wedding shoot options

When researching photographers:
1. Match the photographer's style to the couple's vision
2. Compare packages including hours of coverage, edited photos, albums, prints
3. Note turnaround times for final edited photos
4. Consider second shooter availability and video options
5. Check availability for the wedding date and key events

Always provide structured, actionable recommendations with clear pricing and package details."""

log.info("Initializing PhotographyAgent...")
photography_agent = create_agent(
    model=groq_model,
    tools=[photographer_search, portfolio_review, photography_packages],
    name="PhotographyAgent",
    system_prompt=PHOTOGRAPHY_AGENT_PROMPT,
)


@tool
def delegate_to_photography_agent(query: str) -> str:
    """Delegate photography research tasks to the PhotographyAgent. Use this tool when you need to find photographers, compare packages, or review portfolios."""
    log.info(f"Delegating to PhotographyAgent: {query}")
    response = photography_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
