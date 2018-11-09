from headers.ip_header import IpHeader
from packets.quic_packets.long_packets import LongPacket
from packets.quic_packets.long_packets import LongPacketType
from headers.udp_header import UdpHeader


class InitialPacket(LongPacket):
    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 version,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 token_length,
                 token,
                 length,
                 packet_number,
                 payload):
        super().__init__(ip_header,
                         udp_header,
                         LongPacketType.INITIAL_PACKET,
                         version,
                         dcil,
                         scil,
                         destination_connection_id,
                         source_connection_id)
        self.token_length = token_length
        self.token = token
        self.length = length
        self.packet_number = packet_number
        self.payload = payload
