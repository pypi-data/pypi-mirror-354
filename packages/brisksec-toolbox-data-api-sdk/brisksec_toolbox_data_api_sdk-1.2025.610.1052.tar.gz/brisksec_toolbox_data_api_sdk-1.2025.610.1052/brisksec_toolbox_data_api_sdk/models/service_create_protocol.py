from enum import Enum


class ServiceCreateProtocol(str, Enum):
    ICMP = "icmp"
    TCP = "tcp"
    UDP = "udp"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
