import random
from typing import List

import numpy

from connections.sub_connection import SubConnection
from utils.utils import generate_random_ip, generate_random_string


class Connection:
    MIN_PACKETS = 1
    MAX_PACKETS = 1000

    def __init__(self,
                 start_time,
                 end_time,
                 client_number):
        self.client_number = client_number
        self.end_time = end_time
        self.start_time = start_time
        self.packet_times: List = []
        self.__generate_packets()

    def __generate_packets(self):
        n = random.randint(Connection.MIN_PACKETS, Connection.MAX_PACKETS)
        rate = (self.end_time - self.start_time) / n
        self.packet_times.append(self.start_time)  # add init packet time
        while self.packet_times[-1] < self.end_time:
            time = self.packet_times[-1] + numpy.random.exponential(rate)
            if time > self.end_time:
                break
            # add packet time if it is during the connection's lifetime
            self.packet_times.append(time)
        self.packet_times.append(self.end_time)  # add close packet time

