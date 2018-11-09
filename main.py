from scapy.all import *

from connections_tracker import ConnectionsTracker
from global_connections_manager import GlobalConnectionsManager
from ip_header import IpHeader
from packets.short_packets.short_packet import ShortPacket
from tcp_packet import TcpPacket, TcpFlag
from tcp_parser import TcpParser

# short_p = ShortPacket(123, 1, "encrypted payload")
# print(short_p.header_form)
# print(short_p.destination_connection_id)
# print(short_p.packet_number)
# print(short_p.payload)

#  long_p = LongPacket(1)

gcm = GlobalConnectionsManager()
ip_header1 = IpHeader(20, 5, "132.68.40.13", "216.58.206.3")
ip_header2 = IpHeader(20, 5, "132.68.40.13", "216.255.255.455")
ip_header3 = IpHeader(20, 5, "132.14.14.14", "216.255.255.455")
s_port = 10
d_port = 443
p1 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, "")
# p2 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.ACK], 256, 123, 0, "")
# p3 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [], 256, 123, 0, "")
p4 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [TcpFlag.FIN], 256, 123, 0, "")
# p5 = TcpPacket(ip_header2, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, "")
p6 = TcpPacket(ip_header3, s_port, d_port, 0, 0, 20, [TcpFlag.SYN], 256, 123, 0, "")
p7 = TcpPacket(ip_header1, s_port, d_port, 0, 0, 20, [], 256, 123, 0, "")
p_l = [p1, p6, p4, p7]
for pa in p_l:
    gcm.get_tcp_packet(pa)


packets = rdpcap('captures/example.pcap')
parser = TcpParser()
print(packets[0][1].fields)
tcp_packet = parser.parse(packets[9])
# print(packets[0][2].fields)
# for p in packets:
#     # print(p[2].direction)
#     if p[2].name == "TCP":
#         print(p[2].dport)
print(tcp_packet.source_port)
print(tcp_packet.destination_port)
print(tcp_packet.sequence_number)
print(tcp_packet.ack_number)
print(tcp_packet.header_length)
print(tcp_packet.flags)
print(tcp_packet.window_size)
print(tcp_packet.checksum)
print(tcp_packet.urgent_pointer)
print(tcp_packet.options)

ct = ConnectionsTracker()
ct.start_tracking()
print("the program should continue")
time.sleep(15)
ct.stop_tracking()
print("program ended.")
