from headers.ip_header import IpHeader
from packets.quic_packets.quic_packet import QuicPacket
from headers.udp_header import UdpHeader


class ShortPacket(QuicPacket):
    HEADER_FORM = 0b0
    RESERVED_BITS_VALUE = 0b0000000

    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 destination_connection_id,
                 packet_number,
                 payload):
        super().__init__(ip_header,
                         udp_header,
                         ShortPacket.HEADER_FORM,
                         ShortPacket.RESERVED_BITS_VALUE,
                         destination_connection_id)
        self.packet_number = packet_number
        self.payload = payload
