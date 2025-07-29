from enum import Enum


class ServiceCreateLifecycleStage(str, Enum):
    DEVELOPMENT = "development"
    END_OF_LIFE = "end_of_life"
    MAINTENANCE = "maintenance"
    PLANNING = "planning"
    PRODUCTION = "production"
    RETIRED = "retired"
    TESTING = "testing"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
