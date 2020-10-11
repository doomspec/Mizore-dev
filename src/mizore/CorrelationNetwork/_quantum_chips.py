import networkx as nx


def IBM_5Q_Yorktown(weights=[1.0 for i in range(6)]):
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
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=weights)
    return G


def Rigetti_8Q_Agave(weights=[1.0 for i in range(8)]):
    G = nx.Graph()
    n = 8
    G.add_nodes_from(range(n))
    for i in range(n - 1):
        G.add_edge(i, i + 1, weight=weights[i])
    G.add_edge(n - 1, 0, weight=weights[-1])
    return G


def Rigetti_16Q_Aspen(weights=[1.0 for i in range(18)]):
    G = nx.Graph()
    n = 16
    G.add_nodes_from(range(n))
    for i in range(7):
        G.add_edge(i, i + 1, weight=weights[i])
        G.add_edge(i + 8, i + 9, weight=weights[i + 8])
    G.add_edge(7, 0, weight=weights[7])
    G.add_edge(15, 8, weight=weights[15])
    G.add_edge(0, 15, weight=weights[16])
    G.add_edge(1, 14, weight=weights[17])
    return G


def IBM_20Q_Johannesburg(weights=[1.0 for i in range(25)]):
    G = nx.Graph()
    n = 20
    G.add_nodes_from(range(n))
    for i in range(n - 1):
        G.add_edge(i, i + 1, weight=weights[i])
    for i in range(3):
        G.add_edge(5 * i, 5 * i + 9, weight=weights[20 + i])
    G.add_edge(7, 12, weight=weights[24])
    return G


def Google_Bristlecone(weights=[1.0 for i in range(123)]):
    G = nx.Graph()
    n = 72
    G.add_nodes_from(range(n))
    for j in range(5):
        for i in range(5):
            G.add_edge(36 + (5 * j + i), (6 * j + i), weight=weights[4 * (5 * j + i)])
            G.add_edge(36 + (5 * j + i), (6 * j + i) + 1, weight=weights[4 * (5 * j + i) + 1])
            G.add_edge(36 + (5 * j + i), (6 * j + i) + 6, weight=weights[4 * (5 * j + i) + 2])
            G.add_edge(36 + (5 * j + i), (6 * j + i) + 7, weight=weights[4 * (5 * j + i) + 3])
    for i in range(5):
        G.add_edge(61 + i, 6 * i + 5, weight=weights[100 + 2 * i])
        G.add_edge(61 + i, 6 * i + 11, weight=weights[101 + 2 * i])
    for i in range(5):
        G.add_edge(66 + i, 30 + i, weight=weights[110 + 2 * i])
        G.add_edge(66 + i, 31 + i, weight=weights[111 + 2 * i])
    G.add_edge(71, 35, weight=weights[122])
    return G
