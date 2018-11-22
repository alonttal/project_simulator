from headers.ip_header import IpHeader
from packets.quic_packets.quic_packet import QuicPacket

# Version Negotiation Packet does not count as a Long Packet
from headers.udp_header import UdpHeader


class VersionNegotiationPacket(QuicPacket):
    HEADER_FORM = 1
    UNUSED_BITS_VALUE = 0b0000000
    VERSION_VALUE = 0x00000000  # version MUST be set to 0

    def __init__(self,
                 ip_header: IpHeader,
                 udp_header: UdpHeader,
                 dcil,
                 scil,
                 destination_connection_id,
                 source_connection_id,
                 supported_versions):
        super().__init__(ip_header,
                         udp_header,
                         VersionNegotiationPacket.HEADER_FORM,
                         VersionNegotiationPacket.UNUSED_BITS_VALUE,
                         destination_connection_id)
        self.version = VersionNegotiationPacket.VERSION_VALUE
        self.dcil = dcil
        self.scil = scil
        self.source_connection_id = source_connection_id
        self.supported_versions = supported_versions
