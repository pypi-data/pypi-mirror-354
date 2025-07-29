from enum import Enum


class IPAddressUpdateStatus(str, Enum):
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
