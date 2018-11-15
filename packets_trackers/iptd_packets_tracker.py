from typing import Dict

from packets.quic_packets.quic_packet import QuicPacket
from packets_trackers.packets_tacker import PacketsTracker
from utils import ConnectionId


class ConnectionsMapEntry:
    def __init__(self,
                 last_packet_timestamp,
                 source_ip,
                 destination_ip):
        self.last_packet_timestamp = last_packet_timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.packets_seen = 1
        self.expectation = 0
        self.variance = 0


# Inter-Packet Transmission Delay Packets Tracker
class IptdPacketsTracker(PacketsTracker):
    IPTD_EXTRA_DELTA = 0
    NEW_CONNECTION_IPDT_TIME = 15

    def __init__(self):
        self.__active_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}
        self.__closed_connections_map: Dict[ConnectionId, ConnectionsMapEntry] = {}

    def __update_connection_entry(self, entry, packet_receive_time):
        iptd_delta = packet_receive_time - entry.last_packet_timestamp
        entry.last_packet_timestamp = packet_receive_time
        entry.expectation = (entry.expectation * entry.packets_seen + iptd_delta) / (entry.packets_seen + 1)
        entry.variance = (entry.variance * (entry.packets_seen - 1) + (iptd_delta - entry.expectation) ** 2) \
                         / entry.packets_seen
        entry.packets_seen += 1

    def find_and_remove_dead_connections(self, current_time):
        closed_connections = []
        for k, v in self.__active_connections_map.items():
            max_iptd_time = v.expectation + (v.variance ** 0.5) + IptdPacketsTracker.IPTD_EXTRA_DELTA
            if max_iptd_time == IptdPacketsTracker.IPTD_EXTRA_DELTA:  # for the first packet
                max_iptd_time = IptdPacketsTracker.NEW_CONNECTION_IPDT_TIME
            if current_time - v.last_packet_timestamp > max_iptd_time:
                closed_connections.append(k)
        for k in closed_connections:
            v = self.__active_connections_map.pop(k)
            self.__closed_connections_map.update({k: v})
        #print("IPTD Tacker: closed connections: " + str(len(self.__closed_connections_map)))

    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        destination_connection_id = quic_packet.destination_connection_id
        active_connections_map_entry = self.__active_connections_map.get(destination_connection_id)
        if active_connections_map_entry is not None:  # if an old connection
            self.__update_connection_entry(active_connections_map_entry, packet_receive_time)
        else:  # if new connection
            closed_connections_map_entry = self.__closed_connections_map.pop(destination_connection_id, None)
            if closed_connections_map_entry is not None:
                self.__update_connection_entry(closed_connections_map_entry, packet_receive_time)
                # TODO: maybe need to consider situation where entry is in closed connections map for a long time
                self.__active_connections_map.update({destination_connection_id: closed_connections_map_entry})
            else:
                source_ip = quic_packet.ip_header.source_ip
                destination_ip = quic_packet.ip_header.destination_ip
                new_connections_map_entry = ConnectionsMapEntry(packet_receive_time,
                                                                source_ip,
                                                                destination_ip)
                self.__active_connections_map.update({destination_connection_id: new_connections_map_entry})
        self.find_and_remove_dead_connections(packet_receive_time)  # remove idle connections from active map

    def get_number_of_active_connections(self):
        return len(self.__active_connections_map)
