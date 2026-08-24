from wedding_planner.agents.venue_agent import venue_agent, delegate_to_venue_agent
from wedding_planner.agents.catering_agent import catering_agent, delegate_to_catering_agent
from wedding_planner.agents.photography_agent import photography_agent, delegate_to_photography_agent
from wedding_planner.agents.budget_agent import budget_agent, delegate_to_budget_agent
from wedding_planner.agents.design_agent import design_agent, delegate_to_design_agent
from wedding_planner.agents.timeline_agent import timeline_agent, delegate_to_timeline_agent
from wedding_planner.agents.travel_agent import travel_agent, delegate_to_travel_agent
from wedding_planner.agents.guest_agent import guest_agent, delegate_to_guest_agent
import logging

log = logging.getLogger(__name__)

AGENT_REGISTRY = {
    "venue": {"agent": venue_agent, "tool": delegate_to_venue_agent, "name": "VenueAgent"},
    "catering": {"agent": catering_agent, "tool": delegate_to_catering_agent, "name": "CateringAgent"},
    "photography": {"agent": photography_agent, "tool": delegate_to_photography_agent, "name": "PhotographyAgent"},
    "budget": {"agent": budget_agent, "tool": delegate_to_budget_agent, "name": "BudgetAgent"},
    "design": {"agent": design_agent, "tool": delegate_to_design_agent, "name": "DesignAgent"},
    "timeline": {"agent": timeline_agent, "tool": delegate_to_timeline_agent, "name": "TimelineAgent"},
    "travel": {"agent": travel_agent, "tool": delegate_to_travel_agent, "name": "TravelAgent"},
    "guest": {"agent": guest_agent, "tool": delegate_to_guest_agent, "name": "GuestAgent"},
}

ALL_DELEGATION_TOOLS = [entry["tool"] for entry in AGENT_REGISTRY.values()]

log.info(f"Agent registry loaded: {', '.join(AGENT_REGISTRY.keys())}")
