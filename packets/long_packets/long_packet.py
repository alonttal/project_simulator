from packets.quic_packet import QuicPacket
from packets.long_packets.long_packet_types import LongPacketType
from udp_header import UdpHeader
from ip_header import IpHeader


class LongPacket(QuicPacket):
    HEADER_FORM = 1

    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 packet_type: LongPacketType,
                 version,
                 dcil,  # destination connection id length
                 scil,  # source connection id length
                 destination_connection_id,
                 source_connection_id):
        super().__init__(ip_header,
                         udp_header,
                         ip_header,
                         udp_header,
                         LongPacket.HEADER_FORM,
                         packet_type,
                         destination_connection_id)
        self.version = version
        self.dcil = dcil
        self.scil = scil
        self.source_connection_id = source_connection_id
