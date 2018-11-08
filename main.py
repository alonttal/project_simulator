from scapy.all import *

from connections_tracker import ConnectionsTracker
from packets.short_packets.short_packet import ShortPacket
from tcp_parser import TcpParser

short_p = ShortPacket(123, 1, "encrypted payload")
print(short_p.header_form)
print(short_p.destination_connection_id)
print(short_p.packet_number)
print(short_p.payload)

#  long_p = LongPacket(1)

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
