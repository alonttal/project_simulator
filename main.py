import sys

from generators.connection_generator import ConnectionGenerator
from linkers.ips_linker import IpsLinker
from managers.connections_manager import ConnectionsManager

connection_establishment_parameter = float(sys.argv[1])
connection_life_time_parameter = float(sys.argv[2])
number_of_clients = int(sys.argv[3])

print("Simulation started with: "
      "lambda=" + str(connection_establishment_parameter) +
      ", mu=" + str(connection_life_time_parameter) +
      ", N=" + str(number_of_clients))

connection_generator = ConnectionGenerator(connection_establishment_parameter,
                                           connection_life_time_parameter,
                                           number_of_clients)
connections_manager = ConnectionsManager(number_of_clients)
ips_linker = IpsLinker()

for i in range(0, 2):
    connection = connection_generator.generate()
    sub_connections = connections_manager.generate_sub_connections(i, connection)
    # print("created sub connections of client: " + str(connection.client_number))
    ips_linker.add_sub_connections(sub_connections)

res = ips_linker.try_to_link_ips()
print("Passed" if res == 1 else "Failed")
print("")
