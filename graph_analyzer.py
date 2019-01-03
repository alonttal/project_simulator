import networkx as nx
import matplotlib.pyplot as plt


class GraphAnalyzer:
    def __init__(self):
        self.graph = nx.DiGraph(directed=True)
        self.initial_vertices = []

    def calc_weight(self, cur_ip, other_ip):
        return -(1 - abs(cur_ip.initial_num + cur_ip.non_initial_num - other_ip.non_initial_num) / \
                 (cur_ip.initial_num + cur_ip.non_initial_num + other_ip.non_initial_num) + \
                 cur_ip.start_time / other_ip.start_time)

    def build_graph(self, ips):  # ips is 1D list of ips
        for cur_ip in ips:
            if cur_ip.initial_num + cur_ip.non_initial_num == 0:
                continue
            if cur_ip.non_initial_num == 0:
                self.initial_vertices.append(cur_ip)
            for other_ip in ips:
                if cur_ip.end_time <= other_ip.start_time and other_ip.non_initial_num + other_ip.initial_num > 0:
                    weight = self.calc_weight(cur_ip, other_ip)
                    self.graph.add_edge(cur_ip, other_ip, weight=weight)

    def get_weight(self, path):
        weight = 0
        for i in range(0, len(path) - 1):
            weight += self.graph.edges[(path[i], path[i + 1])]['weight']
        return weight

    def relax(self, u, v, distances, parents):
        if distances.get(v) > distances.get(u) + self.graph.edges[(u, v)]['weight']:
            distances[v] = distances.get(u) + self.graph.edges[(u, v)]['weight']
            parents[v] = u

    def find_max_weight_paths(self):
        distances = {}
        parents = {}
        sorted_vertices = nx.topological_sort(self.graph)
        for u in self.graph.nodes:
            distances.update({u: 0})
            parents.update({u: None})
        for u in sorted_vertices:
            for v in self.graph.neighbors(u):
                self.relax(u, v, distances, parents)
        return parents

    def analyze(self):
        parents = self.find_max_weight_paths()
        res_graph = nx.DiGraph(directed=True)
        for u in parents:
            res_graph.add_node(u)
            if parents[u] is None:
                continue
            res_graph.add_edge(parents[u], u)
        res_graph = self.match_vertices(res_graph)
        res = {}
        for v in res_graph.edges:
            res.update({v[0]: v[1]})
        return res



    def match_vertices(self, graph):
        self.initial_vertices.sort(key=lambda x: x.start_time, reverse=True)
        # nx.draw(graph, with_labels=True)
        # plt.show()
        res_graph = nx.DiGraph(directed=True)
        for u in self.initial_vertices:
            heaviest_path = [u]
            max_weight = 1
            # print(start_vertex)
            for v in graph.nodes:
                # print(end_vertex)
                paths = nx.all_simple_paths(graph, u, v)
                for path in paths:
                    # print(path)
                    path_weight = self.get_weight(path)
                    if path_weight < max_weight:
                        heaviest_path = path
                        max_weight = path_weight
            graph.remove_nodes_from(heaviest_path)
            res_graph.add_path(heaviest_path)
            # res_graph.add_path(list(map(lambda x: "client_num=" + str(x.belongs_to_client) + "\nstart_time=" + str(
            #     x.start_time) + "\nend_time=" + str(x.end_time) + "\ninitial_num=" + str(
            #     x.initial_num) + "\nnon_initial_num=" + str(x.non_initial_num), heaviest_path)))
            # print("===============================")
            # print("Max weight: " + str(max_weight))
            # print("Path: " + str(heaviest_path))
        # nx.draw(res_graph, with_labels=True)
        # plt.show()
        return res_graph

