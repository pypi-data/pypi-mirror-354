from enum import Enum


class ServiceResponseProtocol(str, Enum):
    ICMP = "icmp"
    TCP = "tcp"
    UDP = "udp"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
