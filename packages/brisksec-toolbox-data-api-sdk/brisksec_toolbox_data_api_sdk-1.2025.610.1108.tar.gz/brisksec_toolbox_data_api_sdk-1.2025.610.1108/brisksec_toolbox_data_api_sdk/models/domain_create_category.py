from enum import Enum


class DomainCreateCategory(str, Enum):
    BUSINESS = "business"
    COMPLIANCE = "compliance"
    CUSTOMER = "customer"
    DEVELOPMENT = "development"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"
    PRODUCTION = "production"
    SECURITY = "security"
    TESTING = "testing"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
