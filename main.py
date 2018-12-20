import sys

from generators.connection_generator import ConnectionGenerator
from linkers.ips_linker import IpsLinker
from managers.connections_manager import ConnectionsManager
from managers.expected_connection_time_manager import ExpectedConnectionTimeManager

connection_establishment_parameter = float(sys.argv[1])
connection_life_time_parameter = float(sys.argv[2])
number_of_clients = int(sys.argv[3])
expected_connection_time = int(sys.argv[4]) if len(sys.argv) > 4 else 0

print("Simulation started with: "
      "lambda=" + str(connection_establishment_parameter) +
      ", mu=" + str(connection_life_time_parameter) +
      ", N=" + str(number_of_clients))

connection_generator = ConnectionGenerator(connection_establishment_parameter,
                                           connection_life_time_parameter,
                                           number_of_clients)
connections_manager = ConnectionsManager(number_of_clients)
expected_connection_time_manager = ExpectedConnectionTimeManager()
ips_linker = IpsLinker()

for i in range(0, 50):
    connection = connection_generator.generate()
    sub_connections = connections_manager.generate_sub_connections(i, connection)
    # print("created sub connections of client: " + str(connection.client_number))
    ips_linker.add_sub_connections(sub_connections)
    if expected_connection_time == 0:
        expected_connection_time_manager.add_sub_connections(sub_connections)

if expected_connection_time == 0:
    expected_connection_time = expected_connection_time_manager.calculate_expected_connection_time()
print("Expected connection lifetime is: " + str(expected_connection_time))
res = ips_linker.try_to_link_ips(expected_connection_time)
print("Passed" if res == 1 else "Failed")
print("")
