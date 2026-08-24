from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable

from langchain.messages import HumanMessage

from wedding_planner.cache import cached_tavily_search
from wedding_planner.models import DomainReport, PipelineResult, groq_model
from wedding_planner.prompts import (
    BUDGET_SYNTHESIS_PROMPT,
    CATERING_SYNTHESIS_PROMPT,
    DESIGN_SYNTHESIS_PROMPT,
    GUEST_SYNTHESIS_PROMPT,
    PHOTOGRAPHY_SYNTHESIS_PROMPT,
    SYNTHESIS_PROMPT,
    TIMELINE_SYNTHESIS_PROMPT,
    TRAVEL_SYNTHESIS_PROMPT,
    VENUE_SYNTHESIS_PROMPT,
)
from wedding_planner.retry import CircuitBreaker, retry_on_api_error

log = logging.getLogger(__name__)

ProgressCallback = Callable[[str, str, str], None]


@dataclass
class DomainTask:
    """A single domain research task."""

    domain: str
    tavily_query_fn: Callable[[str], str]
    synthesis_prompt: str


def _build_venue_query(requirements: str) -> str:
    location = _extract_field(requirements, "Wedding location")
    guests = _extract_field(requirements, "Guest count")
    budget = _extract_field(requirements, "Budget range")
    style = _extract_field(requirements, "Preferred style")
    return f"best wedding venues {location} {guests} guests {style} style {budget} budget 2025 2026"


def _build_catering_query(requirements: str) -> str:
    location = _extract_field(requirements, "Wedding location")
    guests = _extract_field(requirements, "Guest count")
    budget = _extract_field(requirements, "Budget range")
    return f"best wedding catering {location} {guests} guests {budget} budget per person price 2025 2026"


def _build_photography_query(requirements: str) -> str:
    location = _extract_field(requirements, "Wedding location")
    style = _extract_field(requirements, "Preferred style")
    budget = _extract_field(requirements, "Budget range")
    return f"best wedding photographers {location} {style} style {budget} budget packages 2025 2026"


def _build_budget_query(requirements: str) -> str:
    location = _extract_field(requirements, "Wedding location")
    guests = _extract_field(requirements, "Guest count")
    budget = _extract_field(requirements, "Budget range")
    return f"wedding budget breakdown allocation percentage {budget} total {guests} guests {location} average costs 2025 2026"


def _build_design_query(requirements: str) -> str:
    style = _extract_field(requirements, "Preferred style")
    return f"wedding color palette floral arrangements {style} style trending colors decor 2025 2026"


def _build_timeline_query(requirements: str) -> str:
    date = _extract_field(requirements, "Target date")
    return f"wedding planning timeline checklist milestones deadlines {date} months out tasks"


def _build_travel_query(requirements: str) -> str:
    location = _extract_field(requirements, "Wedding location")
    guests = _extract_field(requirements, "Guest count")
    return f"hotels near {location} wedding venue group rates {guests} rooms block booking transportation"


def _build_guest_query(requirements: str) -> str:
    guests = _extract_field(requirements, "Guest count")
    return f"wedding RSVP tracking seating chart strategies {guests} guests dietary requirements management"


def _extract_field(requirements: str, field_name: str) -> str:
    """Extract a field value from the requirements text."""
    for line in requirements.split("\n"):
        if field_name.lower() in line.lower() and ":" in line:
            return line.split(":", 1)[1].strip()
    return ""


DOMAIN_TASKS: list[DomainTask] = [
    DomainTask("venue", _build_venue_query, VENUE_SYNTHESIS_PROMPT),
    DomainTask("catering", _build_catering_query, CATERING_SYNTHESIS_PROMPT),
    DomainTask("photography", _build_photography_query, PHOTOGRAPHY_SYNTHESIS_PROMPT),
    DomainTask("budget", _build_budget_query, BUDGET_SYNTHESIS_PROMPT),
    DomainTask("design", _build_design_query, DESIGN_SYNTHESIS_PROMPT),
    DomainTask("timeline", _build_timeline_query, TIMELINE_SYNTHESIS_PROMPT),
    DomainTask("travel", _build_travel_query, TRAVEL_SYNTHESIS_PROMPT),
    DomainTask("guest", _build_guest_query, GUEST_SYNTHESIS_PROMPT),
]

_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)


@retry_on_api_error
def _run_domain_search(task: DomainTask, requirements: str) -> str:
    """Run Tavily search for a domain with caching and retry."""
    query = task.tavily_query_fn(requirements)
    return cached_tavily_search(query, max_results=5)


@retry_on_api_error
def _run_domain_synthesis(task: DomainTask, requirements: str, search_results: str) -> str:
    """Run LLM synthesis for a domain with retry."""
    prompt = task.synthesis_prompt.format(
        requirements=requirements, search_results=search_results
    )
    response = groq_model.invoke([HumanMessage(content=prompt)])
    return response.content


def run_domain_task(
    task: DomainTask,
    requirements: str,
    progress_callback: ProgressCallback | None = None,
) -> DomainReport:
    """Execute a single domain: Tavily search → LLM synthesis. Returns DomainReport."""
    start = time.perf_counter()
    domain_display = task.domain.capitalize() + "Agent"

    if progress_callback:
        progress_callback(task.domain, "running", f"{domain_display} researching...")

    try:
        search_results = _circuit_breaker.call(_run_domain_search, task, requirements)
        log.info(f"[{task.domain}] Tavily search complete ({time.perf_counter() - start:.1f}s)")

        content = _circuit_breaker.call(_run_domain_synthesis, task, requirements, search_results)
        log.info(f"[{task.domain}] LLM synthesis complete ({time.perf_counter() - start:.1f}s)")

        latency = time.perf_counter() - start
        summary = content[:200].strip()
        recommendations = [
            line.strip().lstrip("- ")
            for line in content.split("\n")
            if line.strip().startswith("- ") or line.strip().startswith("* ")
        ][:5]

        report = DomainReport(
            domain=task.domain,
            summary=summary,
            recommendations=recommendations or [summary],
            raw_content=content,
            latency_seconds=round(latency, 2),
            success=True,
        )

        if progress_callback:
            progress_callback(task.domain, "complete", f"{domain_display} done ({latency:.1f}s)")

        return report

    except Exception as exc:
        latency = time.perf_counter() - start
        log.error(f"[{task.domain}] Failed after {latency:.1f}s: {exc}")

        if progress_callback:
            progress_callback(task.domain, "failed", f"{domain_display} failed: {exc}")

        return DomainReport(
            domain=task.domain,
            summary=f"Research failed: {exc}",
            recommendations=[],
            raw_content="",
            latency_seconds=round(latency, 2),
            success=False,
            error=str(exc),
        )


def run_all_domains(
    requirements: str,
    progress_callback: ProgressCallback | None = None,
) -> list[DomainReport]:
    """Run all 8 domain tasks in parallel. Returns list of DomainReports."""
    reports: list[DomainReport] = []

    with ThreadPoolExecutor(max_workers=8, thread_name_prefix="domain") as executor:
        future_to_task = {
            executor.submit(run_domain_task, task, requirements, progress_callback): task
            for task in DOMAIN_TASKS
        }

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                report = future.result()
                reports.append(report)
            except Exception as exc:
                log.error(f"[{task.domain}] Unexpected error: {exc}")
                reports.append(
                    DomainReport(
                        domain=task.domain,
                        summary=f"Unexpected error: {exc}",
                        recommendations=[],
                        raw_content="",
                        latency_seconds=0,
                        success=False,
                        error=str(exc),
                    )
                )

    reports.sort(key=lambda r: DOMAIN_TASKS.index(next(t for t in DOMAIN_TASKS if t.domain == r.domain)))
    return reports


@retry_on_api_error
def synthesize_plan(requirements: str, reports: list[DomainReport]) -> str:
    """Combine all domain reports into the final wedding plan. Single LLM call."""
    report_map = {r.domain: r.raw_content for r in reports}
    prompt = SYNTHESIS_PROMPT.format(
        requirements=requirements,
        venue_report=report_map.get("venue", "No venue research available."),
        catering_report=report_map.get("catering", "No catering research available."),
        photography_report=report_map.get("photography", "No photography research available."),
        budget_report=report_map.get("budget", "No budget research available."),
        design_report=report_map.get("design", "No design research available."),
        timeline_report=report_map.get("timeline", "No timeline research available."),
        travel_report=report_map.get("travel", "No travel research available."),
        guest_report=report_map.get("guest", "No guest management research available."),
    )
    response = groq_model.invoke([HumanMessage(content=prompt)])
    return response.content


def invoke_pipeline(
    requirements: str,
    progress_callback: ProgressCallback | None = None,
) -> PipelineResult:
    """Execute the full parallel pipeline: 8 parallel domains → synthesis → final plan."""
    pipeline_start = time.perf_counter()

    if progress_callback:
        progress_callback("pipeline", "running", "Starting 8 parallel domain research tasks...")

    domain_reports = run_all_domains(requirements, progress_callback)

    successful = sum(1 for r in domain_reports if r.success)
    failed = len(domain_reports) - successful
    log.info(f"Domain research complete: {successful} succeeded, {failed} failed")

    if progress_callback:
        progress_callback("pipeline", "running", f"Synthesizing final plan from {successful} domain reports...")

    try:
        plan = synthesize_plan(requirements, domain_reports)
    except Exception as exc:
        log.error(f"Synthesis failed: {exc}")
        plan = f"# Wedding Plan (Partial)\n\nSynthesis failed: {exc}\n\n## Domain Research Results\n\n"
        for report in domain_reports:
            if report.success:
                plan += f"### {report.domain.capitalize()}\n{report.raw_content}\n\n"

    total_latency = time.perf_counter() - pipeline_start

    if progress_callback:
        progress_callback("pipeline", "complete", f"Plan ready ({total_latency:.1f}s)")

    return PipelineResult(
        plan=plan,
        domain_reports=domain_reports,
        total_latency_seconds=round(total_latency, 2),
        requirements=requirements,
        success=successful > 0,
    )
