from __future__ import annotations

import logging

from wedding_planner.pipeline import invoke_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

log.info("asking user for their requirements...")
user_requirements = input("Please enter your requirements and preferences for your wedding: ")

log.info("invoking parallel pipeline with 8 domain researchers...")
result = invoke_pipeline(user_requirements)

print("\n=== Wedding Plan ===")
print(result.plan)
print(f"\n--- Pipeline completed in {result.total_latency_seconds:.1f}s ---")
for report in result.domain_reports:
    status = "✓" if report.success else "✗"
    print(f"  {status} {report.domain.capitalize()}: {report.latency_seconds:.1f}s")