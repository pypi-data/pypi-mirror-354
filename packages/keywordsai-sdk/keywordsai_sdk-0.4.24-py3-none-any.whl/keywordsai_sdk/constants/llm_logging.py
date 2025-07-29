from django.db import models
from opentelemetry.semconv_ai import LLMRequestTypeValues, TraceloopSpanKindValues
from enum import Enum

class LogMethodChoices(models.TextChoices):
    INFERENCE = "inference"  # Log from a generation api call postprocessing
    LOGGING_API = "logging_api"  # Log from a direct logging API call
    BATCH = "batch"  # Log from a batch create api call
    PYTHON_TRACING = "python_tracing"  # Log from a python tracing call
    TS_TRACING = "ts_tracing"  # Log from a typescript tracing call

class LogTypeChoices(models.TextChoices):
    TEXT = "text"
    RESPONSE = "response" # OpenAI Response API
    EMBEDDING = "embedding"
    TRANSCRIPTION = "transcription"
    SPEECH = "speech"
    WORKFLOW = "workflow"
    TASK = "task"
    TOOL = "tool" # Same as task
    AGENT = "agent" # Same as workflow
    HANDOFF = "handoff" # OpenAI Agent
    GUARDRAIL = "guardrail" # OpenAI Agent
    FUNCTION = "function" # OpenAI Agent
    CUSTOM = "custom" # OpenAI Agent
    GENERATION = "generation" # OpenAI Agent
    UNKNOWN = "unknown"

class SpanKind(Enum):
    TASK = TraceloopSpanKindValues.TASK.value
    WORKFLOW = TraceloopSpanKindValues.WORKFLOW.value
    AGENT = TraceloopSpanKindValues.AGENT.value
    TOOL = TraceloopSpanKindValues.TOOL.value
    CHAT = LLMRequestTypeValues.CHAT.value
    COMPLETION = LLMRequestTypeValues.COMPLETION.value
    EMBEDDING = LLMRequestTypeValues.EMBEDDING.value
    RERANK = LLMRequestTypeValues.RERANK.value
    UNKNOWN = TraceloopSpanKindValues.UNKNOWN.value

SPAN_KIND_TO_LOG_TYPE_MAP = {
    SpanKind.WORKFLOW: LogTypeChoices.WORKFLOW,
    SpanKind.TASK: LogTypeChoices.TASK,
    SpanKind.TOOL: LogTypeChoices.TOOL,
    SpanKind.AGENT: LogTypeChoices.AGENT,
    SpanKind.CHAT: LogTypeChoices.TEXT,
    SpanKind.COMPLETION: LogTypeChoices.TEXT,
    SpanKind.EMBEDDING: LogTypeChoices.EMBEDDING,
    SpanKind.RERANK: LogTypeChoices.UNKNOWN, # Temporary as of 2025-01-20
    SpanKind.UNKNOWN: LogTypeChoices.UNKNOWN,
}
