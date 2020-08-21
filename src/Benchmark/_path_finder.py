import networkx as nx
import itertools
import numpy as np
import copy


def generate_graph(size=10):
    nodes = [str(x) for x in range(size)]
    g = nx.Graph()
    combines = itertools.combinations(nodes, 2)
    for item in combines:
        from_node, to_node = item
        weight = np.random.random()
        g.add_edge(from_node, to_node, weight=weight)
    return g


def find_path_recursive(G, u, n):
    if n == 0:
        return [[u]]
    paths = [[u] + path for neighbor in G.neighbors(u) for path in find_path_recursive(G, neighbor, n - 1) if
             u not in path]
    return paths


def find_path(g: nx.Graph, length: int):
    paths = []
    for node in g.nodes:
        for size in range(1, length + 1):
            paths.extend(find_path_recursive(g, node, size))
    return paths


g = generate_graph(10)
find_path(g, 3)
