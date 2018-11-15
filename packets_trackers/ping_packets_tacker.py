from typing import Dict

from packets.quic_packets.long_packets.long_packet_types import LongPacketType
from packets.quic_packets.quic_packet import QuicPacket
from packets_trackers.packets_tacker import PacketsTracker
from utils import ConnectionId


class ConnectionsMapEntry:
    def __init__(self,
                 initial_packet_seen,
                 last_packet_timestamp,
                 source_ip,
                 destination_ip):
        self.initial_packet_seen = initial_packet_seen
        self.last_packet_timestamp = last_packet_timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip


class PingPongPacketsTracker(PacketsTracker):
    # It is recommended to send a message at least once in 15 seconds to
    # prevent from middle boxes' records to be dropped.
    # There is also an Idle time parameters which is sent in the Initial packets
    # that specifies the timeout for an idle connection
    MAX_IDLE_TIME = 16

    def __init__(self):
        self.__active_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}
        self.__closed_connections_map: Dict[(ConnectionId, ConnectionsMapEntry)] = {}

    def find_and_remove_dead_connections(self, current_time):
        closed_connections = []
        for k, v in self.__active_connections_map.items():
            if current_time - v.last_packet_timestamp > PingPongPacketsTracker.MAX_IDLE_TIME:
                closed_connections.append(k)
        for k in closed_connections:
            v = self.__active_connections_map.pop(k)
            self.__closed_connections_map.update({k: v})
        print("Ping Pong Tacker: closed connections: " + str(len(self.__closed_connections_map)))

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        active_connections_map_entry = self.__active_connections_map.get(destination_connection_id)
        if active_connections_map_entry is not None:  # if a old connection
            active_connections_map_entry.last_packet_timestamp = packet_receive_time
        else:  # if new connection
            # remove from closed connection map
            closed_connections_map_entry = self.__closed_connections_map.pop(destination_connection_id, None)
            if closed_connections_map_entry is not None:
                closed_connections_map_entry.last_packet_timestamp = packet_receive_time
                self.__active_connections_map.update({destination_connection_id: closed_connections_map_entry})
            else:
                is_initial_packet = (quic_packet.reserved_bits == LongPacketType.INITIAL_PACKET)
                source_ip = quic_packet.ip_header.source_ip
                destination_ip = quic_packet.ip_header.destination_ip
                new_connections_map_entry = ConnectionsMapEntry(is_initial_packet,
                                                                packet_receive_time,
                                                                source_ip,
                                                                destination_ip)
                self.__active_connections_map.update({destination_connection_id: new_connections_map_entry})
        self.find_and_remove_dead_connections(packet_receive_time)  # remove idle connections from active map

    def get_number_of_active_connections(self):
        return len(self.__active_connections_map)
