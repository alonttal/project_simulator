from headers.ip_header import IpHeader
from packets.quic_packets.long_packets import LongPacket
from packets.quic_packets.long_packets import LongPacketType
from headers.udp_header import UdpHeader


class RetryPacket(LongPacket):
    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 version,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 odcil,  # original destination connection id length
                 original_destination_connection_id,
                 retry_token):
        super().__init__(ip_header,
                         udp_header,
                         LongPacketType.RETRY_PACKET,
                         version,
                         dcil,
                         scil,
                         destination_connection_id,
                         source_connection_id)
        self.odcil = odcil
        self.original_destination_connection_id = original_destination_connection_id
        self.retry_token = retry_token
