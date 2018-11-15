from typing import List, Dict

from packets.quic_packets.long_packets.long_packet_types import LongPacketType
from packets.quic_packets.quic_packet import QuicPacket
from packets_trackers.packets_tacker import PacketsTracker
from utils import ConnectionId


class ConnectionsMapEntry:
    def __init__(self,
                 first_packet_timestamp,
                 last_packet_timestamp):
        self.first_packet_timestamp = first_packet_timestamp
        self.last_packet_timestamp = last_packet_timestamp
        self.closed_sub_connection_timestamp = None


class EnhancedSubConnectionsPacketsTracker(PacketsTracker):
    DEFAULT_EXPECTED_SUB_CONNECTION_TIME = 15
    EXPECTED_DEAD_SUB_CONNECTION_FACTOR = 2
    MINIMUM_NUMBER_OF_CLOSED_SAMPLES = 20

    def __init__(self):
        self.sum_of_sub_connection_time = 0
        self.__active_sub_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}
        self.__active_sub_connections_list: List[(ConnectionId, ConnectionsMapEntry)] = []
        self.__closed_sub_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}

    def find_and_remove_dead_connections(self, current_time):
        # get the estimated sub-connection time. Note that we use a multiplication factor to refine the time.
        estimated_sub_connection_time = (EnhancedSubConnectionsPacketsTracker.DEFAULT_EXPECTED_SUB_CONNECTION_TIME
                                         if len(self.__closed_sub_connections_map) <= EnhancedSubConnectionsPacketsTracker.MINIMUM_NUMBER_OF_CLOSED_SAMPLES
                                         else self.sum_of_sub_connection_time / len(self.__closed_sub_connections_map))\
                                        * EnhancedSubConnectionsPacketsTracker.EXPECTED_DEAD_SUB_CONNECTION_FACTOR
        new_active_sub_connections_map = {}
        new_active_sub_connections_list = []
        for record in self.__active_sub_connections_list:
            idle_time = current_time - record[1].last_packet_timestamp
            sub_connection_time = record[1].last_packet_timestamp - record[1].first_packet_timestamp
            if idle_time <= estimated_sub_connection_time and sub_connection_time <= estimated_sub_connection_time:
                new_active_sub_connections_map.update({record[0]: record[1]})
                # it is important to keep the original order of the list
                new_active_sub_connections_list.append(record)
            else:
                # we assume that the close connection time is the time of last packet seen
                record[1].closed_sub_connection_timestamp = record[1].last_packet_timestamp
                self.__closed_sub_connections_map.update({record[0]: record[1]})
                self.sum_of_sub_connection_time += record[1].last_packet_timestamp - record[1].first_packet_timestamp
        self.__active_sub_connections_map = new_active_sub_connections_map
        self.__active_sub_connections_list = new_active_sub_connections_list

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        active_sub_connections_map_entry = self.__active_sub_connections_map.get(destination_connection_id)
        closed_sub_connections_map_entry = self.__closed_sub_connections_map.get(destination_connection_id)
        if active_sub_connections_map_entry is not None:  # if an old sub-connection and active
            active_sub_connections_map_entry.last_packet_timestamp = packet_receive_time
        elif closed_sub_connections_map_entry is None:  # if a new sub-connection (not active nor closed)
            is_initial_packet = (quic_packet.reserved_bits == LongPacketType.INITIAL_PACKET)
            # if it is a packet with a new connection-id but it is not an Initial Packet, it means some old connection
            # has changed it's connection-id
            if not is_initial_packet and len(self.__active_sub_connections_list) > 0:
                # we assume that the connection with the oldest arriving time has changed its connection-id
                sub_connection_record = self.__active_sub_connections_list.pop(0)
                self.__active_sub_connections_map.pop(sub_connection_record[0])
                # save the closing time of the sub connection
                sub_connection_record[1].closed_sub_connection_timestamp = packet_receive_time
                self.__closed_sub_connections_map.update({sub_connection_record[0]: sub_connection_record[1]})
                self.sum_of_sub_connection_time += packet_receive_time - sub_connection_record[1].first_packet_timestamp
            new_sub_connection_entry = ConnectionsMapEntry(packet_receive_time, packet_receive_time)
            self.__active_sub_connections_map.update({destination_connection_id: new_sub_connection_entry})
            self.__active_sub_connections_list.append((destination_connection_id, new_sub_connection_entry))
        self.find_and_remove_dead_connections(packet_receive_time)

    def get_number_of_active_connections(self):
        return len(self.__active_sub_connections_map)
