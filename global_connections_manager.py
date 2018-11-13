from typing import Dict, List

from packets.tcp_packets.tcp_packet import TcpPacket, TcpFlag
from converters.tcp_to_quic_packet_converter import TcpToQuicPacketConverter
from utils import generate_random_string


class GlobalConnectionsMapEntry:
    def __init__(self,
                 destination_ip,
                 source_connection_id,
                 destination_connection_id,
                 quic_version,
                 current_source_ip):
        self.destination_ip = destination_ip
        self.source_connection_id = source_connection_id
        self.destination_connection_id = destination_connection_id
        self.quic_version = quic_version
        self.current_source_ip = current_source_ip

    def get_number_of_connections(self):
        pass


class GlobalConnectionsManager:
    DEFAULT_SOURCE_CONNECTION_ID_LENGTH = 64
    DEFAULT_DESTINATION_CONNECTION_ID_LENGTH = 64
    DEFAULT_QUIC_VERSION = "1"

    def __init__(self):
        self.__global_connections_map: Dict[str, GlobalConnectionsMapEntry] = {}
        self.__closed_connections_map: List[(str, GlobalConnectionsMapEntry)] = []

    def get_quic_packet(self, tcp_packet: TcpPacket):
        print("new packet received")
        # TODO: need to randomly generate a new connection id
        # TODO: allow injection of probability functions
        packet = None
        source_ip = tcp_packet.ip_header.source_ip
        destination_ip = tcp_packet.ip_header.destination_ip
        global_connection_map_entry = self.__global_connections_map.get(source_ip)
        if global_connection_map_entry is None:  # not in map
            print("new connection detected")
            if TcpFlag.SYN in tcp_packet.flags and TcpFlag.ACK not in tcp_packet.flags:
                print("it is a SYN packet. adding to map")
                quic_version = GlobalConnectionsManager.DEFAULT_QUIC_VERSION
                source_connection_id = generate_random_string(
                    GlobalConnectionsManager.DEFAULT_SOURCE_CONNECTION_ID_LENGTH)
                destination_connection_id = generate_random_string(
                    GlobalConnectionsManager.DEFAULT_DESTINATION_CONNECTION_ID_LENGTH)
                new_global_connection_map_entry = GlobalConnectionsMapEntry(destination_ip,
                                                                            source_connection_id,
                                                                            destination_connection_id,
                                                                            quic_version,
                                                                            source_ip)
                self.__global_connections_map.update({source_ip: new_global_connection_map_entry})
                packet = TcpToQuicPacketConverter().convert_to_initial_packet(tcp_packet,
                                                                              quic_version,
                                                                              destination_connection_id,
                                                                              source_connection_id)
        else:  # in map
            print("the source ip is known")
            if global_connection_map_entry.destination_ip == destination_ip:  # track only a single connection
                print("connection is known")
                packet = TcpToQuicPacketConverter() \
                    .convert_to_short_packet(tcp_packet, global_connection_map_entry.destination_connection_id)
                if TcpFlag.FIN in tcp_packet.flags:
                    print("it is a FIN packet. removing from map")
                    self.__closed_connections_map.append((source_ip, global_connection_map_entry))
                    print("adding FIN packet to closed connections list. size of list is: " +
                          str(len(self.__closed_connections_map)))
                    self.__global_connections_map.pop(source_ip)
        return packet

    def get_number_of_connections(self):
        return len(self.__global_connections_map)
