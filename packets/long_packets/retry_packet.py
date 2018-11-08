from packets.long_packets.long_packet import LongPacket
from packets.long_packets.long_packet_types import LongPacketType


class RetryPacket(LongPacket):
    def __init__(self,
                 version,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 odcil,  # original destination connection id length
                 original_destination_connection_id,
                 retry_token):
        super().__init__(LongPacketType.RETRY_PACKET,
                         version,
                         dcil,
                         scil,
                         destination_connection_id,
                         source_connection_id)
        self.odcil = odcil
        self.original_destination_connection_id = original_destination_connection_id
        self.retry_token = retry_token
