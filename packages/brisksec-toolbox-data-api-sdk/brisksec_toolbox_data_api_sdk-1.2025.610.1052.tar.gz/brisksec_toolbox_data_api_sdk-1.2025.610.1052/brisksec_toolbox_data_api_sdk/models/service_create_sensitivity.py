from enum import Enum


class ServiceCreateSensitivity(str, Enum):
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"
    PUBLIC = "public"
    UNKNOWN = "unknown"
    VERY_HIGH = "very_high"

    def __str__(self) -> str:
        return str(self.value)
