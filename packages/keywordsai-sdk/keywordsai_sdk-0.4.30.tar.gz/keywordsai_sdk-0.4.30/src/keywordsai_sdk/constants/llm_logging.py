from enum import Enum

class KeywordsAISpanAttributes(Enum):
    LOG_METHOD = "keywordsai.entity.log_method"
    LOG_TYPE = "keywordsai.entity.log_type"
    LOG_ID = "keywordsai.entity.log_id"
    LOG_PARENT_ID = "keywordsai.entity.log_parent_id"
    LOG_ROOT_ID = "keywordsai.entity.log_root_id"
    LOG_SOURCE = "keywordsai.entity.log_source"

class LogMethodChoices(Enum):
    INFERENCE = "inference"  # Log from a generation api call postprocessing
    LOGGING_API = "logging_api"  # Log from a direct logging API call
    BATCH = "batch"  # Log from a batch create api call
    PYTHON_TRACING = "python_tracing"  # Log from a python tracing call
    TS_TRACING = "ts_tracing"  # Log from a typescript tracing call

class LogTypeChoices(Enum):
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