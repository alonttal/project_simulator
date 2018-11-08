from packets.packet import Packet
from packets.long_packets.long_packet_types import LongPacketType


class LongPacket(Packet):
    HEADER_FORM = 1

    def __init__(self,
                 packet_type: LongPacketType,
                 version,
                 dcil,  # destination connection id length
                 scil,  # source connection id length
                 destination_connection_id,
                 source_connection_id):
        super().__init__(LongPacket.HEADER_FORM, packet_type, destination_connection_id)
        self.version = version
        self.dcil = dcil
        self.scil = scil
        self.source_connection_id = source_connection_id

