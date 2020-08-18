from GA._ga_constructor import GAConstructor
import networkx as nx
import itertools
import numpy as np


def generate_graph(size=10):
    nodes = [str(x) for x in range(size)]
    g = nx.Graph()
    combines = itertools.combinations(nodes, 2)
    for item in combines:
        from_node, to_node = item
        weight = np.random.random()
        g.add_edge(from_node, to_node, weight=weight)
    return g


g = generate_graph()
ga = GAConstructor(g)
ga.run(time_budget=10)
