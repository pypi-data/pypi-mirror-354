from enum import Enum

class RunStatus(str, Enum):
    DRAFT = "draft"
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class RunResultResponseFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"