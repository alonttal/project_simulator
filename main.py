from scapy.all import *

from connections_tracker import ConnectionsTracker
from packets.short_packets.short_packet import ShortPacket

short_p = ShortPacket(123, 1, "encrypted payload")
print(short_p.header_form)
print(short_p.destination_connection_id)
print(short_p.packet_number)
print(short_p.payload)

#  long_p = LongPacket(1)

packets = rdpcap('captures/example.pcap')
print(packets[0][2].fields)
for p in packets:
    # print(p[2].direction)
    if p[2].name == "TCP":
        print(p[2].dport)


ct = ConnectionsTracker()
ct.start_tracking()
print("the program should continue")
time.sleep(15)
ct.stop_tracking()
print("program ended.")
