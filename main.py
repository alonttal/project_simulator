from graph_analyzer import GraphAnalyzer
from params import Params
from traffic_builder import TrafficBuilder


traffic_builder = TrafficBuilder(Params.CLIENTS_NUM, Params.CONNECTIONS_NUM, Params.SUB_CONNECTIONS_PER_CONNECTION)
traffic = traffic_builder.build()
# for t in traffic[0]:
#     print(str(t.__dict__))
ips = [t for sublist in traffic for t in sublist]
graph_analyzer = GraphAnalyzer()
graph_analyzer.build_graph(ips)
res = graph_analyzer.analyze()


correct = 0
incorrect = 0
for u in res:
    if u.belongs_to_client != res[u].belongs_to_client:
        incorrect += 1
    else:
        correct += 1
print("Correct: " + str(correct) + ", Incorrect: " + str(incorrect))

