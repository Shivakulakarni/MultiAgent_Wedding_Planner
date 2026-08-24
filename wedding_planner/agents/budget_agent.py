from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from wedding_planner.models import groq_model
from wedding_planner.tools.budget_tools import budget_breakdown, cost_comparison, savings_tips
import logging

log = logging.getLogger(__name__)

BUDGET_AGENT_PROMPT = """You are an expert wedding budget specialist. Your role is to help couples optimize their wedding budget and maximize value.

Your expertise includes:
- Creating detailed budget breakdowns across all wedding categories
- Finding cost-saving opportunities without sacrificing quality
- Comparing vendor pricing and negotiating strategies
- Tracking expenses and managing budget overruns
- Recommending contingency funds and payment schedules

When managing budgets:
1. Start with the total budget and allocate percentages to each category
2. Consider the couple's priorities for higher allocation
3. Identify areas where savings are possible without impacting the experience
4. Compare at least 3 options in each category when possible
5. Include tips for timing purchases, off-peak savings, and negotiation

Typical budget allocation guidelines:
- Venue & Catering: 40-50%
- Photography & Videography: 10-15%
- Flowers & Decor: 8-12%
- Music & Entertainment: 8-10%
- Attire & Beauty: 8-10%
- Stationery & Favors: 3-5%
- Contingency: 5-10%

Always provide actionable, specific recommendations with dollar amounts or percentages."""

log.info("Initializing BudgetAgent...")
budget_agent = create_agent(
    model=groq_model,
    tools=[budget_breakdown, cost_comparison, savings_tips],
    name="BudgetAgent",
    system_prompt=BUDGET_AGENT_PROMPT,
)


@tool
def delegate_to_budget_agent(query: str) -> str:
    """Delegate budget planning and cost optimization tasks to the BudgetAgent. Use this tool when you need budget breakdowns, cost comparisons, or savings recommendations."""
    log.info(f"Delegating to BudgetAgent: {query}")
    response = budget_agent.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content
