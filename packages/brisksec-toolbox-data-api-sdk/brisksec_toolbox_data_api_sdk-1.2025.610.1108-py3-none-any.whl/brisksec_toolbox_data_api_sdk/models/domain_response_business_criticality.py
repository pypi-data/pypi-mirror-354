from enum import Enum


class DomainResponseBusinessCriticality(str, Enum):
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"
    MISSION_CRITICAL = "mission_critical"
    NONE = "none"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
