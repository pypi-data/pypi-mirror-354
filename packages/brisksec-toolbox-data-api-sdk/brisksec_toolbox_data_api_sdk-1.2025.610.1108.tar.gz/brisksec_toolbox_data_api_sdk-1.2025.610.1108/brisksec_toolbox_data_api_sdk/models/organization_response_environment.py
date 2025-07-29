from enum import Enum


class OrganizationResponseEnvironment(str, Enum):
    DEMO = "demo"
    DEVELOPMENT = "development"
    DR = "dr"
    PRODUCTION = "production"
    SANDBOX = "sandbox"
    STAGING = "staging"
    TESTING = "testing"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
