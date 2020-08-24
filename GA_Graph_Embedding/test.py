from GA_Graph_Embedding._ga_constructor import GAConstructor
import networkx as nx
import itertools
import numpy as np
import time


def generate_graph(size=10):
    nodes = [str(x) for x in range(size)]
    g = nx.Graph()
    combines = itertools.combinations(nodes, 2)
    for item in combines:
        from_node, to_node = item
        weight = np.random.random()
        g.add_edge(from_node, to_node, weight=weight)
    return g


g = generate_graph(10)
ga = GAConstructor(g,generate_graph(11))
ga.run(time_budget=120)
res = ga.get_result()
# print(res)