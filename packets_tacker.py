from packets.quic_packets.quic_packet import QuicPacket


class PacketsTracker:
    def track_packet(self, quic_packet: QuicPacket, packet_receive_time):
        pass

    def get_number_of_active_connections(self):
        pass
