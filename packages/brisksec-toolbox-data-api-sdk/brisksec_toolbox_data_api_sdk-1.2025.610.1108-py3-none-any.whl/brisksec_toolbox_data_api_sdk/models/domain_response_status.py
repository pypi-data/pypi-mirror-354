from enum import Enum


class DomainResponseStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    DEPRECATED = "deprecated"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    PLANNED = "planned"
    PROVISIONING = "provisioning"
    RETIRED = "retired"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
