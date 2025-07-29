from enum import Enum


class ServiceUpdateProtocol(str, Enum):
    ICMP = "icmp"
    TCP = "tcp"
    UDP = "udp"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
