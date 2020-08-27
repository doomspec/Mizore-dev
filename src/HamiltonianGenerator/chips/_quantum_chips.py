import networkx as nx

def IBM_5Q_Yorktown(weights=[1,1,1,1,1,1]):
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

def Rigetti_8Q_Agave(weights=[0.975, 0.975, 0.975, 0.975, 0.975, 0.975, 0.975, 0.975]):
    G = nx.Graph()
    n = 8
    G.add_nodes_from(range(n))
    for i in range(n-1):
        G.add_edge(i, i+1, weight = weights[i])
    G.add_edge(n-1, 0, weight = weights[-1])
    return G

def Rigetti_16Q_Aspen(weights=[0.975 for i in range(18)]):
    G = nx.Graph()
    n = 16
    G.add_nodes_from(range(n))
    for i in range(7):
        G.add_edge(i, i+1, weight = weights[i])
        G.add_edge(i+8, i+9, weight = weights[i+8])
    G.add_edge(7, 0, weight = weights[7])
    G.add_edge(15, 8, weight = weights[15])
    G.add_edge(0, 15, weight = weights[16])
    G.add_edge(1, 14, weight = weights[17])
    return G