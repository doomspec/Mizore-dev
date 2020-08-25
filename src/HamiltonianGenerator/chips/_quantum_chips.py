import Networkx as nx

def IBM5QYorktown(weights=None):
    G = nx.Graph()
    G.add_nodes_from(range(5))
    if len(weights) == 6:
        G.add_weighted_edges_from([(0, 1, weights[0]), (0, 2, weights[1]), (1, 2, weights[2])
            , (2, 3, weights[3]), (2, 4, weights[4]), (3, 4, weights[5])])
    else:
        G.add_weighted_edges_from([(0, 1, 1), (0, 2, 1), (1, 2, 1)
            , (2, 3, 1), (2, 4, 1), (3, 4, 1)])
    return G