from __future__ import annotations

import logging

from wedding_planner.pipeline import DomainTask, DOMAIN_TASKS

log = logging.getLogger(__name__)

AGENT_REGISTRY = {
    task.domain: {"name": f"{task.domain.capitalize()}Agent", "task": task}
    for task in DOMAIN_TASKS
}

ALL_DELEGATION_TOOLS: list = []

log.info(f"Agent registry loaded: {', '.join(AGENT_REGISTRY.keys())}")
