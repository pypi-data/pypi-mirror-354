from enum import Enum


class IPAddressResponseEnvironment(str, Enum):
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
