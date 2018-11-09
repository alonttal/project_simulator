from enum import Enum
from headers.ip_header import IpHeader


class TcpFlag(Enum):
    ACK = 4
    RST = 6
    SYN = 7
    FIN = 8


class TcpPacket:
    def __init__(self,
                 ip_header: IpHeader,
                 source_port,
                 destination_port,
                 sequence_number,
                 ack_number,
                 header_length,  # in dwords
                 flags,
                 window_size,
                 checksum,
                 urgent_pointer,
                 options):
        self.ip_header = ip_header
        self.source_port = source_port
        self.destination_port = destination_port
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.header_length = header_length
        self.flags = flags
        self.window_size = window_size
        self.checksum = checksum
        self.urgent_pointer = urgent_pointer
        self.options = options
