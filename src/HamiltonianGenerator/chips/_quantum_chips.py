import Networkx as nx

def IBM5QYorktown(weights=[1,1,1,1,1,1]):
    G = nx.Graph()
    G.add_nodes_from(range(5))
    G.add_weighted_edges_from([(0, 1, weights[0]), (0, 2, weights[1]), (1, 2, weights[2])
            , (2, 3, weights[3]), (2, 4, weights[4]), (3, 4, weights[5])])
    return G

def ionq_full_connected(weights=0.975):
    G = nx.Graph()
    n = 11
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            G.add_edge(i, j, weight = weights)
    return G