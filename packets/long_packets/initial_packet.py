from packets.long_packets.long_packet import LongPacket
from packets.long_packets.long_packet_types import LongPacketType


class InitialPacket(LongPacket):
    def __init__(self,
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
        super().__init__(LongPacketType.INITIAL_PACKET,
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
