# Count the number of initial sub-connections and number of non-initial sub-connections and calculate the average
# sub-connections of a single connection by the formula (Y/X) where Y is the total non-initial sub-connections and X
# is the total initial sub-connections.
# The total connection time is therefore (Y/X + 1) * [expected life time of a sub-connection].
# We here calculate the expected life time of a sub-connection by averaging the subtraction of the last packet seen time
# and the first packet seen time of all the sub-connections.
from typing import Dict

from packets.quic_packets.long_packets.long_packet_types import LongPacketType
from packets.quic_packets.quic_packet import QuicPacket
from packets_trackers.packets_tacker import PacketsTracker
from utils import ConnectionId


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
        self.__sub_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}

    def __get_connection_estimated_time(self):
        # this is [expected life time of a sub-connection] * (Y/X + 1)
        return self.sum_of_sub_connection_time / self.number_of_initial_packets

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        sub_connections_map_entry = self.__sub_connections_map.get(destination_connection_id)
        if sub_connections_map_entry is not None:  # if an old connection
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

    def get_number_of_active_connections(self, current_time):
        number_of_active_connections = 0
        expected_sub_connection_time = self.sum_of_sub_connection_time / len(self.__sub_connections_map)
        for k, v in self.__sub_connections_map.items():
            if current_time - v.first_packet_timestamp < expected_sub_connection_time:
                number_of_active_connections += 1
        print("SubConnectionsPacketsTracker: estimated time for sub connection: " + str(sub_connection_time) +
              " number of connections: " + str(number_of_active_connections))
        return number_of_active_connections
