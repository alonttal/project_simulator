from typing import List

from connections.sub_connection import SubConnection


class ExpectedConnectionTimeManager:

    def __init__(self):
        self.X = 0
        self.Y = 0
        self.total_time = 0

    def add_sub_connections(self, sub_connections_list: List[SubConnection]):
        self.Y += len(sub_connections_list) - 1
        self.X += 1
        for sub_connection in sub_connections_list:
            self.total_time += sub_connection.end_time - sub_connection.start_time

    def calculate_expected_connection_time(self):
        return self.total_time / self.X
