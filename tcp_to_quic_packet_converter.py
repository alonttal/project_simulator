from packets.quic_packets.long_packets.handshake_packet import HandshakePacket
from packets.quic_packets.long_packets.initial_packet import InitialPacket
from packets.quic_packets.other_packets.version_negotiation_packet import VersionNegotiationPacket
from packets.quic_packets.short_packets.short_packet import ShortPacket
from packets.tcp_packets.tcp_packet import TcpPacket
from headers.udp_header import UdpHeader
from utils import generate_random_string


class TcpToQuicPacketConverter:
    DEFAULT_TOKEN_LENGTH = 32

    def __build_udp_header(self, tcp_packet):
        length = 0  # TODO: change to real length
        checksum = 0
        return UdpHeader(tcp_packet.source_port, tcp_packet.destination_port, length, checksum)

    def convert_to_short_packet(self, tcp_packet: TcpPacket, destination_connection_id):
        udp_header = self.__build_udp_header(tcp_packet)
        packet_number = "encrypted"
        payload = "encrypted"
        return ShortPacket(tcp_packet.ip_header,
                           udp_header,
                           destination_connection_id,
                           packet_number,
                           payload)

    def convert_to_initial_packet(self,
                                  tcp_packet: TcpPacket,
                                  version,
                                  destination_connection_id,
                                  source_connection_id):
        # token value must be set to zero if sent from serve
        token = generate_random_string(TcpToQuicPacketConverter.DEFAULT_TOKEN_LENGTH)
        udp_header = self.__build_udp_header(tcp_packet)
        length = 0  # TODO: change to real length
        packet_number = "encrypted"
        payload = "encrypted"
        return InitialPacket(tcp_packet.ip_header,
                             udp_header,
                             version,
                             len(destination_connection_id),
                             len(source_connection_id),
                             destination_connection_id,
                             source_connection_id,
                             len(token),
                             token,
                             length,
                             packet_number,
                             payload)

    def convert_to_handshake_packet(self,
                                    tcp_packet: TcpPacket,
                                    version,
                                    destination_connection_id,
                                    source_connection_id):
        udp_header = self.__build_udp_header(tcp_packet)
        length = 0  # TODO: change to real length
        packet_number = "encrypted"
        payload = "encrypted"
        return HandshakePacket(tcp_packet.ip_header,
                               udp_header,
                               version,
                               len(destination_connection_id),
                               len(source_connection_id),
                               destination_connection_id,
                               source_connection_id,
                               length,
                               packet_number,
                               payload)

    def convert_to_version_negotiation_packet(self,
                                              tcp_packet: TcpPacket,
                                              destination_connection_id,
                                              source_connection_id,
                                              supported_versions):
        udp_header = self.__build_udp_header(tcp_packet)
        return VersionNegotiationPacket(tcp_packet.ip_header,
                                        udp_header,
                                        len(destination_connection_id),
                                        len(source_connection_id),
                                        destination_connection_id,
                                        source_connection_id,
                                        supported_versions)
