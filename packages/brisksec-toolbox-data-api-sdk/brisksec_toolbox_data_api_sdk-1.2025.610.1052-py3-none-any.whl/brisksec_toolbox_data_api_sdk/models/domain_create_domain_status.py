from enum import Enum


class DomainCreateDomainStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
