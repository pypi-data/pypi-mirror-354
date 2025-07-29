from enum import Enum


class DomainCreateClassification(str, Enum):
    CONFIDENTIAL = "confidential"
    CRITICAL = "critical"
    INTERNAL = "internal"
    PUBLIC = "public"
    REGULATED = "regulated"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
