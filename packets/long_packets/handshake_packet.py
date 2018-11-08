from packets.long_packets.long_packet import LongPacket
from packets.long_packets.long_packet_types import LongPacketType


class HandshakePacket(LongPacket):
    def __init__(self,
                 version,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 length,
                 packet_number,
                 payload):
        super().__init__(LongPacketType.HANDSHAKE_PACKET,
                         version,
                         dcil,
                         scil,
                         destination_connection_id,
                         source_connection_id)
        self.length = length
        self.packet_number = packet_number
        self.payload = payload
