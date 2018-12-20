import random
from typing import List

from connections.sub_connection import SubConnection
from generators.connection_generator import Connection
from packets.quic_packet import QuicPacket
from utils.utils import generate_random_string, generate_random_ip


class ClientIdentity:
    def __init__(self, ip, start_time=0, end_time=0):
        self.ip = ip
        self.start_time = start_time
        self.end_time = end_time


class SubConnectionManager:
    def __init__(self, connection_num, connection: Connection, client_ips):
        self.__connection_num = connection_num
        self.__connection = connection
        self.__client_ips = client_ips
        self.__ip_index = 0
        self.__destination_connection_id = generate_random_string(QuicPacket.DEFAULT_CONNECTION_ID_LENGTH)

    def __should_generate_new_identity(self, packet_time):
        # create a new connection id and ip if there are no identities yet
        # or if the last ip that was created was before this packet time
        return len(self.__client_ips) == 0 or \
               (self.__client_ips[-1].end_time < packet_time and random.random() <= 0.01)

    def __generate_identification(self, time):
        self.__destination_connection_id = generate_random_string(QuicPacket.DEFAULT_CONNECTION_ID_LENGTH)
        self.__client_ips.append(ClientIdentity(generate_random_ip(), time, time))
        self.__ip_index = len(self.__client_ips) - 1

    def __set_ip_index(self, new_index):
        if new_index != self.__ip_index:
            self.__destination_connection_id = generate_random_string(QuicPacket.DEFAULT_CONNECTION_ID_LENGTH)
        self.__ip_index = new_index

    def __get_client_ip(self, packet_time):
        # this should always hold because we are running on connections ordered by their start time
        assert self.__client_ips[0].start_time <= packet_time
        for i in range(self.__ip_index, len(self.__client_ips)):
            ip_start_time = self.__client_ips[i].start_time
            ip_end_time = self.__client_ips[i + 1].start_time if i + 1 < len(self.__client_ips) else float('inf')
            if ip_start_time <= packet_time < ip_end_time:
                self.__set_ip_index(i)
                break
        return self.__client_ips[self.__ip_index].ip

    def __generate_quic_packets(self):
        is_first_packet = True
        last_packet_time = self.__connection.packet_times[0]
        quic_packets: List[QuicPacket] = []
        for packet_time in self.__connection.packet_times:
            if self.__should_generate_new_identity(packet_time):
                # set the ip-time different than the packet-time so that other connections with the same ip will have
                # a chance for their first packet to arrive before this connection's first packet
                time = max(packet_time - (packet_time - last_packet_time) * (random.random() * 0.9), 0)
                self.__generate_identification(time)
            client_ip = self.__get_client_ip(packet_time)
            packet = QuicPacket(client_ip, self.__destination_connection_id, packet_time, is_first_packet)
            quic_packets.append(packet)
            last_packet_time = packet_time
            is_first_packet = False
        if self.__client_ips[-1].end_time < self.__connection.packet_times[-1]:
            self.__client_ips[-1].end_time = self.__connection.packet_times[-1]
        return quic_packets

    def generate_sub_connections(self):
        sub_connections: List[SubConnection] = []
        quic_packets = self.__generate_quic_packets()
        first_packet_index = 0
        for i in range(1, len(quic_packets)):
            if quic_packets[i - 1].destination_connection_id != quic_packets[i].destination_connection_id or\
                    i == len(quic_packets) - 1:
                sub_connection = SubConnection(self.__connection_num,
                                               quic_packets[i - 1].destination_connection_id,
                                               quic_packets[i - 1].source_ip,
                                               quic_packets[first_packet_index].send_time,
                                               quic_packets[i - 1].send_time,
                                               quic_packets[first_packet_index].is_initial)
                sub_connections.append(sub_connection)
                first_packet_index = i
        return sub_connections


class ConnectionsManager:
    def __init__(self, number_of_clients):
        self.__number_of_clients = number_of_clients
        self.__clients_identity: List[List[ClientIdentity]] = []
        self.__init_clients_identity()

    def __init_clients_identity(self):
        for i in range(0, self.__number_of_clients):
            ip = generate_random_ip()
            self.__clients_identity.append([])

    def generate_sub_connections(self, connection_num, connection: Connection):
        client_ips = self.__clients_identity[connection.client_number]
        return SubConnectionManager(connection_num, connection, client_ips).generate_sub_connections()
