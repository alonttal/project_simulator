from typing import Dict

from packets.quic_packets.long_packets.long_packet_types import LongPacketType
from packets.quic_packets.quic_packet import QuicPacket
from utils.utils import ConnectionId


class SubConnectionsEntry:
    def __init__(self,
                 destination_connection_id,
                 source_ip,
                 destination_ip,
                 is_initial,
                 start_timestamp):
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.destination_connection_id = destination_connection_id
        self.is_initial = is_initial
        self.start_timestamp = start_timestamp
        self.end_timestamp = start_timestamp


class Tracker:
    def __init__(self):
        self.sub_connections_map: Dict[ConnectionId, SubConnectionsEntry] = {}

    def track_packet(self, quic_packet: QuicPacket, packet_timestamp):
        destination_connection_id = quic_packet.destination_connection_id
        active_connections_map_entry = self.sub_connections_map.get(destination_connection_id)
        if active_connections_map_entry is not None:  # if a old connection
            active_connections_map_entry.end_timestamp = packet_timestamp
        else:  # if new connection
            is_initial_packet = (quic_packet.reserved_bits == LongPacketType.INITIAL_PACKET)
            source_ip = quic_packet.ip_header.source_ip
            destination_ip = quic_packet.ip_header.destination_ip
            new_sub_connection_entry = SubConnectionsEntry(destination_connection_id,
                                                           source_ip,
                                                           destination_ip,
                                                           is_initial_packet,
                                                           packet_timestamp)
            self.sub_connections_map.update({destination_connection_id: new_sub_connection_entry})
