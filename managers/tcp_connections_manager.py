import random
from typing import Dict, List

from packets.tcp_packets.tcp_packet import TcpPacket, TcpFlag
from converters.tcp_to_quic_packet_converter import TcpToQuicPacketConverter
from utils.utils import generate_random_string, SourceIp, DestinationIp, SourcePort


class TcpConnectionsMapEntry:
    def __init__(self,
                 destination_ip,
                 source_ip,
                 source_port,
                 source_connection_id,
                 destination_connection_id,
                 quic_version,
                 start_timestamp):
        self.destination_ip = destination_ip
        self.source_ips: List = [source_ip]
        self.source_ports: List = [source_port]
        self.source_connection_ids: List = [source_connection_id]
        self.destination_connection_ids: List = [destination_connection_id]
        self.quic_version = quic_version
        self.start_timestamp = start_timestamp
        self.end_timestamp = start_timestamp


class TcpConnectionsManager:
    DEFAULT_SOURCE_CONNECTION_ID_LENGTH = 64
    DEFAULT_DESTINATION_CONNECTION_ID_LENGTH = 64
    DEFAULT_QUIC_VERSION = "1"

    def __init__(self):
        self.connections_map: Dict[(SourceIp, DestinationIp, SourcePort), TcpConnectionsMapEntry] = {}

    def __should_generate_new_connection_id(self):
        return random.random() <= 0.1

    def change_identification(self, entry: TcpConnectionsMapEntry, tcp_packet):
        new_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        new_port = str(random.randint(0, 32000))
        new_src_id = generate_random_string(TcpConnectionsManager.DEFAULT_SOURCE_CONNECTION_ID_LENGTH)
        new_dest_id = generate_random_string(TcpConnectionsManager.DEFAULT_SOURCE_CONNECTION_ID_LENGTH)
        entry.source_connection_ids.append(new_src_id)
        entry.destination_connection_ids.append(new_dest_id)
        entry.source_ips.append(new_ip)
        entry.source_ports.append(new_port)
        tcp_packet.ip_header.source_ip = new_ip
        tcp_packet.source_port = new_port

    def get_quic_packet(self, tcp_packet: TcpPacket, packet_timestamp):
        packet = None
        source_ip = tcp_packet.ip_header.source_ip
        destination_ip = tcp_packet.ip_header.destination_ip
        source_port = tcp_packet.source_port
        key_tuple = (source_ip, destination_ip, source_port)
        connection_map_entry = self.connections_map.get(key_tuple)
        if connection_map_entry is None:  # not in map
            # print("new connection detected")
            if TcpFlag.SYN in tcp_packet.flags and TcpFlag.ACK not in tcp_packet.flags:
                # print("it is a SYN packet. adding to map")
                quic_version = TcpConnectionsManager.DEFAULT_QUIC_VERSION
                source_connection_id = generate_random_string(
                    TcpConnectionsManager.DEFAULT_SOURCE_CONNECTION_ID_LENGTH)
                destination_connection_id = generate_random_string(
                    TcpConnectionsManager.DEFAULT_DESTINATION_CONNECTION_ID_LENGTH)
                new_connection_map_entry = TcpConnectionsMapEntry(destination_ip,
                                                                  source_ip,
                                                                  source_port,
                                                                  source_connection_id,
                                                                  destination_connection_id,
                                                                  quic_version,
                                                                  packet_timestamp)
                self.connections_map.update({key_tuple: new_connection_map_entry})
                packet = TcpToQuicPacketConverter().convert_to_initial_packet(tcp_packet,
                                                                              quic_version,
                                                                              destination_connection_id,
                                                                              source_connection_id)
        else:  # in map
            if self.__should_generate_new_connection_id():
                self.change_identification(connection_map_entry, tcp_packet)
            packet = TcpToQuicPacketConverter() \
                .convert_to_short_packet(tcp_packet, connection_map_entry.destination_connection_ids[-1])
            connection_map_entry.end_timestamp = packet_timestamp
        return packet
