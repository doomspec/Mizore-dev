import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def draw_graph(G: nx.Graph, path="Untitled"):
    pos = nx.spring_layout(G, k=1.5, scale=100)
    nx.draw_networkx_nodes(G, pos, node_color="blue")
    nx.draw_networkx_labels(G, pos, font_color="white")
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    edge_labels = {(u, v): np.round(d["weight"], 2) for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black", alpha=1,
                                 bbox=dict(boxstyle='round',
                                           ec=(1.0, 1.0, 1.0),
                                           fc=(1.0, 1.0, 1.0),
                                           alpha=0.0
                                           ))
    plt.savefig(path + ".png")


def get_nx_graph_by_adjacent_mat(_adjacent_mat, weight_amplifier=100, weight_cutoff=0.1):
    adjacent_mat = np.array(_adjacent_mat)
    adjacent_mat *= weight_amplifier
    G = nx.Graph(adjacent_mat)
    zero_edge = []
    for u, v, d in G.edges(data=True):
        if abs(d["weight"]) < weight_cutoff:
            zero_edge.append((u, v))
    for u, v in zero_edge:
        G.remove_edge(u, v)
    return G
