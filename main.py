from scapy.all import *
from scapy.layers.inet import TCP, IP

from exporter import CsvExporter
from global_connections_manager import GlobalConnectionsManager
from packets_trackers.enhanced_sub_connections_packets_tracker import EnhancedSubConnectionsPacketsTracker
from packets_trackers.iptd_packets_tracker import IptdPacketsTracker
from packets_trackers.ping_packets_tacker import PingPongPacketsTracker
from packets_trackers.sub_connections_packets_tracker import SubConnectionsPacketsTracker
from tcp_parser import TcpParser

# short_p = ShortPacket(123, 1, "encrypted payload")
# print(short_p.header_form)
# print(short_p.destination_connection_id)
# print(short_p.packet_number)
# print(short_p.payload)

#  long_p = LongPacket(1)

# gcm = GlobalConnectionsManager()
# attacker = SimplePacketsTracker()
# ip_header1 = IpHeader(20, 5, "132.68.40.13", "216.58.206.3")
# ip_header2 = IpHeader(20, 5, "132.68.40.13", "216.255.255.455")
# ip_header3 = IpHeader(20, 5, "132.14.14.14", "216.255.255.455")
# s_port = 10
# d_port = 443
# p1 = (1, TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, ""))
# p2 = (1.002584, TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.ACK], 256, 123, 0, ""))
# p3 = (5.095, TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [], 256, 123, 0, ""))
# p4 = (6.315, TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.FIN], 256, 123, 0, ""))
# p5 = (40, TcpPacket(ip_header2, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, ""))
# # p6 = TcpPacket(ip_header3, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, "")
# # p7 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [], 256, 123, 0, "")
# p_l = [p1, p2, p3, p4]
# for pa in p_l:
#     quic_packet = gcm.get_quic_packet(pa[1])
#     if quic_packet is not None:
#         attacker.track_packet(quic_packet, pa[0])
#         print("tracking. # of active connections is: " + str(attacker.get_number_of_active_connections()))
# attacker.find_and_remove_dead_connections(40)
#
# exporter = CsvExporter()
# exporter.export_real_and_estimated_connections('results.csv', [1, 2, 3], [1, 1, 2], [1, 2, 1])
#
print("Starting Simulation")
packet_sampling_times = []
real_number_of_connections = []
estimated_number_of_connections = []
global_connections_manager = GlobalConnectionsManager()
attacker = EnhancedSubConnectionsPacketsTracker()
pcap_reader = PcapReader('captures/example2.pcap')
exporter = CsvExporter('first_experiment.csv')
exporter.clear_file()
exporter.write_headers('times', 'real number of connections', 'estimated number of connections')
counter = 0
for raw_packet in pcap_reader:
    if raw_packet.haslayer(TCP) and raw_packet.haslayer(IP):  # TODO: maybe we need to also support IPv6
        tcp_packet = TcpParser().parse(raw_packet)
        quic_packet = global_connections_manager.get_quic_packet(tcp_packet)
        counter += 1
        if counter % 1000 == 0:
            print("Processed: " + str(counter) + " packets")
            exporter.write('a', packet_sampling_times, real_number_of_connections, estimated_number_of_connections)
            packet_sampling_times.clear()
            real_number_of_connections.clear()
            estimated_number_of_connections.clear()
        if quic_packet is not None:
            attacker.track_packet(quic_packet, raw_packet.time)
            packet_sampling_times.append(raw_packet.time)
            real_number_of_connections.append(global_connections_manager.get_number_of_connections())
            estimated_number_of_connections.append(attacker.get_number_of_active_connections())
print("Finished Simulation")
# packets = rdpcap('captures/example.pcap')
# parser = TcpParser()
# print("time: " + str(packets[0].time))
# print("time: " + str(packets[1].time))
# tcp_packet = parser.parse(packets[9])
# # print(packets[0][2].fields)
# # for p in packets:
# #     # print(p[2].direction)
# #     if p[2].name == "TCP":
# #         print(p[2].dport)
# print(tcp_packet.source_port)
# print(tcp_packet.destination_port)
# print(tcp_packet.sequence_number)
# print(tcp_packet.ack_number)
# print(tcp_packet.header_length)
# print(tcp_packet.flags)
# print(tcp_packet.window_size)
# print(tcp_packet.checksum)
# print(tcp_packet.urgent_pointer)
# print(tcp_packet.options)
#
# ct = ConnectionsTracker()
# ct.start_tracking()
# print("the program should continue")
# time.sleep(15)
# ct.stop_tracking()
# print("program ended.")
