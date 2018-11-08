from ip_header import IpHeader
from packets.long_packets.long_packet import LongPacket
from packets.long_packets.long_packet_types import LongPacketType
from udp_header import UdpHeader


class HandshakePacket(LongPacket):
    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 version,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 length,
                 packet_number,
                 payload):
        super().__init__(ip_header,
                         udp_header,
                         LongPacketType.HANDSHAKE_PACKET,
                         version,
                         dcil,
                         scil,
                         destination_connection_id,
                         source_connection_id)
        self.length = length
        self.packet_number = packet_number
        self.payload = payload
