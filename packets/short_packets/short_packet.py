from packets.packet import Packet


class ShortPacket(Packet):
    HEADER_FORM = 0b0
    RESERVED_BITS_VALUE = 0b0000000

    def __init__(self,
                 destination_connection_id,
                 packet_number,
                 payload):
        super().__init__(ShortPacket.HEADER_FORM, ShortPacket.RESERVED_BITS_VALUE, destination_connection_id)
        self.packet_number = packet_number
        self.payload = payload
