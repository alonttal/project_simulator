import random

import numpy

from connections.connection import Connection


class ConnectionGenerator:
    def __init__(self,
                 connection_establishment_parameter,
                 connection_life_time_parameter,
                 number_of_clients):
        self.__connection_establishment_parameter = connection_establishment_parameter  # lambda
        self.__connection_life_time_parameter = connection_life_time_parameter  # mu
        self.__number_of_clients = number_of_clients  # N
        self.__start_time = 0

    def generate(self):
        self.__start_time += numpy.random.exponential(self.__connection_establishment_parameter)
        end_time = self.__start_time + numpy.random.exponential(self.__connection_life_time_parameter)
        belongs_to_client = random.randint(0, self.__number_of_clients - 1)
        connection = Connection(self.__start_time, end_time, belongs_to_client)
        return connection
