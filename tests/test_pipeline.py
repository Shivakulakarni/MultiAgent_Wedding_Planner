from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest

from wedding_planner.cache import cached_tavily_search, clear_cache, cache_stats
from wedding_planner.models import DomainReport, PipelineResult
from wedding_planner.pipeline import (
    DOMAIN_TASKS,
    invoke_pipeline,
    run_all_domains,
    run_domain_task,
    synthesize_plan,
)
from wedding_planner.retry import CircuitBreaker, retry_on_api_error


class TestCache:
    def setup_method(self) -> None:
        clear_cache()

    def test_cached_tavily_search_miss(self) -> None:
        with patch("wedding_planner.cache.tavily_search") as mock_search:
            mock_search.return_value = "Search results for test query"
            result = cached_tavily_search("test query")
            assert result == "Search results for test query"
            assert mock_search.call_count == 1

    def test_cached_tavily_search_hit(self) -> None:
        with patch("wedding_planner.cache.tavily_search") as mock_search:
            mock_search.return_value = "Search results for test query"
            cached_tavily_search("test query")
            mock_search.return_value = "Different results"
            result = cached_tavily_search("test query")
            assert result == "Search results for test query"
            assert mock_search.call_count == 1

    def test_cached_tavily_search_different_max_results(self) -> None:
        with patch("wedding_planner.cache.tavily_search") as mock_search:
            mock_search.return_value = "Results for 5"
            cached_tavily_search("test query", max_results=5)
            mock_search.return_value = "Results for 3"
            result = cached_tavily_search("test query", max_results=3)
            assert result == "Results for 3"
            assert mock_search.call_count == 2

    def test_cache_stats(self) -> None:
        clear_cache()
        stats = cache_stats()
        assert stats["size"] == 0
        assert stats["maxsize"] == 128
        assert stats["ttl"] == 3600


class TestCircuitBreaker:
    def test_circuit_breaker_opens_after_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

        def fail():
            raise RuntimeError("fail")

        for _ in range(3):
            try:
                cb.call(fail)
            except RuntimeError:
                pass

        assert cb.state == "open"
        with pytest.raises(RuntimeError, match="Circuit breaker is OPEN"):
            cb.call(lambda: "success")

    def test_circuit_breaker_closes_on_success(self) -> None:
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

        def fail():
            raise RuntimeError("fail")

        for _ in range(2):
            try:
                cb.call(fail)
            except RuntimeError:
                pass

        assert cb.call(lambda: "success") == "success"
        assert cb.state == "closed"

    def test_circuit_breaker_half_open_after_timeout(self) -> None:
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0)

        def fail():
            raise RuntimeError("fail")

        for _ in range(2):
            try:
                cb.call(fail)
            except RuntimeError:
                pass

        # Access internal state directly to avoid triggering transition
        assert cb._state == "open"
        time.sleep(0.1)
        # After recovery_timeout=0, accessing state triggers transition to half-open
        assert cb.state == "half-open"


class TestRetry:
    def test_retry_succeeds_after_failure(self) -> None:
        call_count = 0

        @retry_on_api_error
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("temporary failure")
            return "success"

        result = flaky()
        assert result == "success"
        assert call_count == 2

    def test_retry_exhausted(self) -> None:
        @retry_on_api_error
        def always_fail():
            raise ConnectionError("permanent failure")

        with pytest.raises(ConnectionError):
            always_fail()


class TestDomainTask:
    def test_domain_tasks_count(self) -> None:
        assert len(DOMAIN_TASKS) == 8

    def test_domain_tasks_names(self) -> None:
        names = {t.domain for t in DOMAIN_TASKS}
        expected = {"venue", "catering", "photography", "budget", "design", "timeline", "travel", "guest"}
        assert names == expected

    def test_build_queries(self) -> None:
        requirements = """
            Wedding location: Chicago, Illinois
            Guest count: 120
            Budget range: USD 35000 to 65000
            Preferred style: Modern, Romantic
            Target date: 2026-05-15
        """
        for task in DOMAIN_TASKS:
            query = task.tavily_query_fn(requirements)
            assert isinstance(query, str)
            assert len(query) > 10
            # Most queries should contain location or year, but guest query only has guest count
            if task.domain != "guest":
                assert "Chicago" in query or "2025" in query or "2026" in query


class TestPipeline:
    def test_invoke_pipeline_returns_valid_result(self) -> None:
        with patch("wedding_planner.pipeline.groq_model") as mock_model:
            mock_model.invoke.return_value.content = "# Test Plan\n\nExecutive summary here."

            result = invoke_pipeline("test requirements")

            assert isinstance(result, PipelineResult)
            assert result.plan == "# Test Plan\n\nExecutive summary here."
            assert len(result.domain_reports) == 8
            assert result.total_latency_seconds >= 0
            assert result.success is True

    def test_invoke_pipeline_domain_reports_structure(self) -> None:
        with patch("wedding_planner.pipeline.groq_model") as mock_model:
            mock_model.invoke.return_value.content = "SUMMARY: Test\nRECOMMENDATIONS: - Item 1"

            result = invoke_pipeline("test requirements")

            for report in result.domain_reports:
                assert isinstance(report, DomainReport)
                assert report.domain in {"venue", "catering", "photography", "budget", "design", "timeline", "travel", "guest"}
                assert isinstance(report.summary, str)
                assert isinstance(report.recommendations, list)
                assert isinstance(report.raw_content, str)
                assert isinstance(report.latency_seconds, float)
                assert isinstance(report.success, bool)

    def test_synthesize_plan_combines_reports(self) -> None:
        with patch("wedding_planner.pipeline.groq_model") as mock_model:
            mock_model.invoke.return_value.content = "# Final Plan"

            reports = [
                DomainReport(domain="venue", summary="V", recommendations=[], raw_content="Venue content", latency_seconds=1.0, success=True),
                DomainReport(domain="catering", summary="C", recommendations=[], raw_content="Catering content", latency_seconds=1.0, success=True),
            ]
            plan = synthesize_plan("requirements", reports)
            assert plan == "# Final Plan"


class TestDomainReportValidation:
    def test_valid_domain_report(self) -> None:
        report = DomainReport(
            domain="venue",
            summary="Test summary",
            recommendations=["Rec 1", "Rec 2"],
            raw_content="Full content",
            latency_seconds=1.5,
            success=True,
        )
        assert report.domain == "venue"
        assert report.success is True

    def test_failed_domain_report(self) -> None:
        report = DomainReport(
            domain="catering",
            summary="Failed",
            recommendations=[],
            raw_content="",
            latency_seconds=0.5,
            success=False,
            error="API error",
        )
        assert report.success is False
        assert report.error == "API error"


class TestPipelineResultValidation:
    def test_valid_pipeline_result(self) -> None:
        reports = [
            DomainReport(domain="venue", summary="V", recommendations=[], raw_content="", latency_seconds=1.0, success=True),
        ]
        result = PipelineResult(
            plan="Plan",
            domain_reports=reports,
            total_latency_seconds=2.0,
            requirements="Req",
            success=True,
        )
        assert result.success is True
        assert len(result.domain_reports) == 1