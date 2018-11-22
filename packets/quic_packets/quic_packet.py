from headers.udp_header import UdpHeader
from headers.ip_header import IpHeader


class QuicPacket:
    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 header_form,
                 reserved_bits,
                 destination_connection_id):
        self.ip_header = ip_header
        self.udp_header = udp_header
        self.header_form = header_form
        self.reserved_bits = reserved_bits
        self.destination_connection_id = destination_connection_id
