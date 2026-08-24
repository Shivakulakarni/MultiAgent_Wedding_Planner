from __future__ import annotations

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

groq_model = init_chat_model("qwen/qwen3.6-27b", model_provider="groq")


class DomainReport(BaseModel):
    """Structured output from a single domain research task."""

    domain: str = Field(description="Domain name: venue, catering, photography, budget, design, timeline, travel, guest")
    summary: str = Field(description="2-3 sentence domain summary")
    recommendations: list[str] = Field(description="Key recommendations for this domain")
    raw_content: str = Field(description="Full domain research content from LLM")
    latency_seconds: float = Field(description="Time taken for this domain in seconds")
    success: bool = Field(description="Whether domain research succeeded")
    error: str | None = Field(default=None, description="Error message if domain research failed")


class PipelineResult(BaseModel):
    """Complete result from the parallel pipeline execution."""

    plan: str = Field(description="Final synthesized wedding plan (Markdown)")
    domain_reports: list[DomainReport] = Field(description="Per-domain research results")
    total_latency_seconds: float = Field(description="Total pipeline latency in seconds")
    requirements: str = Field(description="Original requirements text")
    success: bool = Field(description="Whether the pipeline completed successfully")
