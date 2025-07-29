from enum import Enum


class ServiceCreateServiceStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    FILTERED = "filtered"
    INACTIVE = "inactive"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
