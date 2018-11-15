# Count the number of initial sub-connections and number of non-initial sub-connections and calculate the average
# sub-connections of a single connection by the formula (Y/X) where Y is the total non-initial sub-connections and X
# is the total initial sub-connections.
# The total connection time is therefore (Y/X + 1) * [expected life time of a sub-connection].
# We here calculate the expected life time of a sub-connection by averaging the subtraction of the last packet seen time
# and the first packet seen time of all the sub-connections.
from typing import Dict, List

from packets.quic_packets.long_packets.long_packet_types import LongPacketType
from packets.quic_packets.quic_packet import QuicPacket
from packets_trackers.packets_tacker import PacketsTracker


class ConnectionsMapEntry:
    def __init__(self,
                 first_packet_timestamp,
                 last_packet_timestamp,
                 source_ip,
                 destination_ip):
        self.first_packet_timestamp = first_packet_timestamp
        self.last_packet_timestamp = last_packet_timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip


class SubConnectionsPacketsTracker(PacketsTracker):
    # DEFAULT_EXPECTED_SUB_CONNECTION_TIME = 30

    def __init__(self):
        self.number_of_initial_packets = 0
        self.number_of_non_initial_packets = 0
        self.sum_of_sub_connection_time = 0
        self.__sub_connections_map: Dict[str, ConnectionsMapEntry] = {}

    def __get_sub_connection_estimated_time(self):
        # this is [expected life time of a sub-connection] * (Y/X + 1)
        return self.sum_of_sub_connection_time / self.number_of_initial_packets

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        sub_connections_map_entry = self.__sub_connections_map.get(destination_connection_id)
        if sub_connections_map_entry is not None:  # if a old connection
            # we are adding the delta lifetime of the sub-connection
            self.sum_of_sub_connection_time += packet_receive_time - sub_connections_map_entry.last_packet_timestamp
            sub_connections_map_entry.last_packet_timestamp = packet_receive_time
        else:  # new connection
            source_ip = quic_packet.ip_header.source_ip
            destination_ip = quic_packet.ip_header.destination_ip
            new_connections_map_entry = ConnectionsMapEntry(packet_receive_time,
                                                            packet_receive_time,
                                                            source_ip,
                                                            destination_ip)
            self.__sub_connections_map.update({destination_connection_id: new_connections_map_entry})
            self.number_of_initial_packets += (quic_packet.reserved_bits == LongPacketType.INITIAL_PACKET)
            self.number_of_non_initial_packets += (quic_packet.reserved_bits != LongPacketType.INITIAL_PACKET)

    def get_number_of_active_connections(self):
        alive_counter = 0
        sub_connection_time = self.__get_sub_connection_estimated_time()
        for k, v in self.__sub_connections_map.items():
            if v.last_packet_timestamp - v.first_packet_timestamp < sub_connection_time:
                alive_counter += 1
        print("estimated time for sub connection: " + str(sub_connection_time) + " number of connections: " + str(alive_counter))
        return alive_counter


class EnhancedSubConnectionsPacketsTracker(PacketsTracker):
    DEFAULT_EXPECTED_SUB_CONNECTION_TIME = 30

    def __init__(self):
        self.number_of_initial_packets = 0
        self.number_of_non_initial_packets = 0
        self.sum_of_sub_connection_time = 0
        self.__active_sub_connections_map: Dict[str, ConnectionsMapEntry] = {}
        self.__close_sub_connections_map: Dict[str, ConnectionsMapEntry] = {}

    def __pop_from_close_sub_connections_map(self, key):
        closed_connections_map_entry = self.__close_sub_connections_map.pop(key, None)
        if closed_connections_map_entry is not None:
            self.sum_of_sub_connection_time -= \
                closed_connections_map_entry.last_packet_timestamp - closed_connections_map_entry.first_packet_timestamp
        return closed_connections_map_entry

    def __update_close_sub_connections_map(self, key, value):
        self.sum_of_sub_connection_time += value.last_packet_timestamp - value.first_packet_timestamp
        self.__close_sub_connections_map.update({key: value})

    def __remove_longest_idle_time_sub_connection(self, current_time):
        longest_idle_time = 0
        longest_idle_connection_id = None
        for k, v in self.__active_sub_connections_map.items():
            idle_time = current_time - v.last_packet_timestamp
            if idle_time > longest_idle_time:
                longest_idle_time = idle_time
                longest_idle_connection_id = k
        entry = self.__active_sub_connections_map.pop(longest_idle_connection_id)
        self.__update_close_sub_connections_map(longest_idle_connection_id, entry)

    def __get_sub_connection_estimated_time(self):
        if len(self.__close_sub_connections_map) == 0:
            return EnhancedSubConnectionsPacketsTracker.DEFAULT_EXPECTED_SUB_CONNECTION_TIME
        else:
            return self.sum_of_sub_connection_time / len(self.__close_sub_connections_map)

    def find_and_remove_dead_sub_connections(self, current_time):
        sub_connection_time = self.__get_sub_connection_estimated_time()
        closed_connections = []
        for k, v in self.__active_sub_connections_map.items():
            if current_time - v.first_packet_timestamp > PingPongPacketsTracker.MAX_IDLE_TIME:
                closed_connections.append(k)
        for k in closed_connections:
            v = self.__active_connections_map.pop(k)
            self.__closed_connections_map.update({k: v})
        print("Ping Pong Tacker: closed connections: " + str(len(self.__closed_connections_map)))

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        sub_connections_map_entry = self.__active_sub_connections_map.get(destination_connection_id)
        if sub_connections_map_entry is not None:  # if a old connection
            sub_connections_map_entry.last_packet_timestamp = packet_receive_time
        else:
            closed_connections_map_entry = self.__pop_from_close_sub_connections_map(destination_connection_id)
            if closed_connections_map_entry is not None:
                closed_connections_map_entry.last_packet_timestamp = packet_receive_time
                self.__active_sub_connections_map.update({destination_connection_id: closed_connections_map_entry})
            else:
                is_initial_packet = (quic_packet.reserved_bits == LongPacketType.INITIAL_PACKET)
                if not is_initial_packet:

                source_ip = quic_packet.ip_header.source_ip
                destination_ip = quic_packet.ip_header.destination_ip
                new_connections_map_entry = ConnectionsMapEntry(packet_receive_time,
                                                                packet_receive_time,
                                                                source_ip,
                                                                destination_ip)
                self.__active_sub_connections_map.update({destination_connection_id: new_connections_map_entry})

    def get_number_of_active_connections(self):
        pass