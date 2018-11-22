import json

from scapy.layers.inet import TCP, IP
from scapy.utils import PcapReader

from managers.tcp_connections_manager import TcpConnectionsManager
from mongo.mongo import manager_collection, tracker_collection
from parsers.tcp_parser import TcpParser
from trackers.tracker import Tracker

print("Starting Simulation...")
tcp_connections_manager = TcpConnectionsManager()
tracker = Tracker()
pcap_reader = PcapReader('captures/example2.pcap')
counter = 0
for raw_packet in pcap_reader:
    if raw_packet.haslayer(TCP) and raw_packet.haslayer(IP):  # TODO: maybe we need to also support IPv6
        counter += 1
        tcp_packet = TcpParser().parse(raw_packet)
        quic_packet = tcp_connections_manager.get_quic_packet(tcp_packet, raw_packet.time)
        if counter % 50000 == 0:
            print("Processed: " + str(counter) + " packets")
        if quic_packet is not None:
            tracker.track_packet(quic_packet, raw_packet.time)
print("Processed: " + str(counter) + " packets")
print("clearing database...")
manager_collection.drop()
tracker_collection.drop()
print("Saving to database...")
for v in tcp_connections_manager.connections_map.values():
    manager_collection.insert(v.__dict__)
for v in tracker.sub_connections_map.values():
    tracker_collection.insert(v.__dict__)
print("Finished Simulation.")
