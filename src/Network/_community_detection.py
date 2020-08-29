import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import infomap
from ._utilities import get_nx_graph_by_adjacent_mat

"""
The functions for community detection and community draw for graphs
"""


def detect_nx_graph_community(g: nx.Graph):
    im = infomap.Infomap()
    nodes = g.nodes
    im.add_nodes(nodes)
    for edge in g.edges:
        res = g[edge[0]][edge[1]]
        weight = res["weight"]
        im.addLink(edge[0], edge[1], 1 / weight)
    im.run("--directed --silent")
    """
    print(f'node num: {len(nodes)}')
    print(f"Found {im.num_top_modules} modules with code length: {im.codelength}")
    print("Result")
    print("node module")
    """
    node_module_map = {}

    for node in im.tree:
        if node.is_leaf:
            node_module_map[node.node_id] = node.module_id

    return node_module_map


def assign_community_color(node_module_map):
    val_map = {}
    colors = ["#ee4035", "#f37736", "#7bc043", "#008744", "#0392cf", "#2a4d69", "#ee4035"]
    node_list = list(node_module_map.keys())
    node_list.sort()
    for node_id in node_list:
        module_id = node_module_map[node_id]
        val_map[module_id] = colors[int(module_id) % len(colors)]
    color_map = [val_map.get(node_module_map[node_id]) for node_id in node_list]
    return color_map


def draw_community_graph(G: nx.Graph, node_module_map, path="Untitled"):
    pos = nx.spring_layout(G, k=1.5, scale=100)
    nx.draw_networkx_nodes(G, pos, node_color=assign_community_color(node_module_map))
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


def convert_node_module_map_to_array(node_module_map):
    arr_dict = {}
    for node in node_module_map.keys():
        mod = node_module_map[node]
        if mod in arr_dict.keys():
            arr_dict[mod].append(node)
        else:
            arr_dict[mod] = [node]

    arr = []
    for mod, nodes in arr_dict.items():
        arr.append(nodes)
    return arr


def detect_community(adjacent_mat):
    G = get_nx_graph_by_adjacent_mat(adjacent_mat)
    return convert_node_module_map_to_array(detect_nx_graph_community(G))


if __name__ == "__main__":
    mi = [[0.0, 0.021162439190284182, 0.012310588191778209, 0.07292515180218262, 0.020901745997648213,
           0.012310987481864308],
          [0.021162439190284182, 0.0, 0.015340506148096098, 0.020901745997648213, 0.014533197324912712,
           0.006273653044042406],
          [0.012310588191778209, 0.015340506148096098, 0.0, 0.012310987481864308, 0.006273653044042406,
           0.005801011165626119],
          [0.07292515180218262, 0.020901745997648213, 0.012310987481864308, 0.0, 0.021162439190284182,
           0.012310588191778209],
          [0.020901745997648213, 0.014533197324912712, 0.006273653044042406, 0.021162439190284182, 0.0,
           0.015340506148096098],
          [0.012310987481864308, 0.006273653044042406, 0.005801011165626119, 0.012310588191778209, 0.015340506148096098,
           0.0]]

    G = get_nx_graph_by_adjacent_mat(mi, weight_cutoff=0.1)
    node_module_map = detect_nx_graph_community(G)

    print(convert_node_module_map_to_array(node_module_map))
    draw_community_graph(G, node_module_map)
