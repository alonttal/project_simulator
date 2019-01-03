import math
import random

import numpy

from ip_window import IpWindow
from params import Params
from utils import generate_random_ip


class TrafficBuilder:
    def __init__(self, clients_num, connections_num, sub_connections_per_connection):
        self.clients_num = clients_num
        self.connections_num = connections_num
        self.sub_connections_per_connection = sub_connections_per_connection

    def generate_ips(self):
        ips = []
        ips_per_client = math.ceil(2 * self.connections_num / self.clients_num * self.sub_connections_per_connection)
        for i in range(0, self.clients_num):
            client_ips = []
            start_time = 0
            for j in range(0, ips_per_client):
                ip = generate_random_ip()
                start_time += numpy.random.exponential(1 / Params.IP_CHANGE_PARAM)
                ip_window = IpWindow(ip, start_time, float('inf'), i)
                if len(client_ips) > 0:
                    client_ips[-1].end_time = start_time
                client_ips.append(ip_window)
            ips.append(client_ips)
        return ips


    def should_exist_in_window(self):
        return random.random() >= Params.SUB_CONNECTION_EXISTS_IN_WINDOW_THRESH

    def generate_connections(self, ips):
        for i in range(0, self.connections_num):
            belongs_to_client = random.randint(0, self.clients_num - 1)
            # print(str(belongs_to_client))
            window_len = random.randint(math.floor(self.sub_connections_per_connection / 2), self.sub_connections_per_connection * 2)
            # print(str(window_len))
            start_window = random.randint(0, len(ips[belongs_to_client]) - window_len)
            # print(str(start_window))
            ips[belongs_to_client][start_window].initial_num += 1
            for j in range(start_window + 1, start_window + window_len):
                if self.should_exist_in_window():
                    ips[belongs_to_client][j].non_initial_num += 1

    def build(self):
        ips = self.generate_ips()
        self.generate_connections(ips)
        return ips

