import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from cdlib import algorithms
from cdlib import viz
import infomap
import itertools


def detect_community(g: nx.Graph):
    im = infomap.Infomap()
    nodes = g.nodes
    colors = ["#ee4035", "#f37736", "#7bc043", "#008744", "#0392cf", "#2a4d69", "#ee4035"]
    im.add_nodes(nodes)
    for edge in g.edges:
        res = g[edge[0]][edge[1]]
        weight = res["weight"]
        im.addLink(edge[0], edge[1], 1 / weight)
    im.run("--directed --silent")
    print(f'node num: {len(nodes)}')
    print(f"Found {im.num_top_modules} modules with codelength: {im.codelength}")

    print("Result")
    print("\n#node module")
    node_module_map = {}
    val_map = {}
    for node in im.tree:
        if node.is_leaf:
            node_module_map[node.node_id] = node.module_id
            val_map[node.module_id] = colors[int(node.module_id) % len(colors)]
            print(node.node_id, node.module_id)

    values = [val_map.get(node_module_map[node]) for node in g.nodes()]
    return values


if __name__ == "__main__":
    mi = [
        [0.0, 0.0538758450985564, 0.02614562320786966, 0.02614562320786966, 0.008245482299012799, 0.007864536298169127,
         0.012310588191778209, 0.012310588191778209],
        [0.0538758450985564, 0.0, 0.02614562320786966, 0.02614562320786966, 0.007864536298169127, 0.008245482299012799,
         0.012310588191778209, 0.012310588191778209],
        [0.02614562320786966, 0.02614562320786966, 0.0, 0.01937679910061013, 1.4832056870604793e-05,
         1.4832056870604793e-05, 0.0003230449833626914, 0.0054519507555633034],
        [0.02614562320786966, 0.02614562320786966, 0.01937679910061013, 0.0, 1.4832056870604793e-05,
         1.4832056870604793e-05, 0.0054519507555633034, 0.0003230449833626914],
        [0.008245482299012799, 0.007864536298169127, 1.4832056870604793e-05, 1.4832056870604793e-05, 0.0,
         0.012592316707630283, 7.282117723543535e-06, 7.282117723543535e-06],
        [0.007864536298169127, 0.008245482299012799, 1.4832056870604793e-05, 1.4832056870604793e-05,
         0.012592316707630283, 0.0, 7.282117723543535e-06, 7.282117723543535e-06],
        [0.012310588191778209, 0.012310588191778209, 0.0003230449833626914, 0.0054519507555633034,
         7.282117723543535e-06, 7.282117723543535e-06, 0.0, 0.005779662736367819],
        [0.012310588191778209, 0.012310588191778209, 0.0054519507555633034, 0.0003230449833626914,
         7.282117723543535e-06, 7.282117723543535e-06, 0.005779662736367819, 0.0]]
    mi = np.array(mi)
    mi *= 100
    G = nx.Graph(mi)
    zero_edge = []
    for u, v, d in G.edges(data=True):
        print(u, v, np.round(d["weight"], 2))
        if abs(d["weight"]) < 0.1:
            zero_edge.append((u, v))
    for u, v in zero_edge:
        G.remove_edge(u, v)
    pos = nx.spring_layout(G, k=0.05, scale=100)
    nx.draw_networkx_nodes(G, pos, node_color=detect_community(G))
    nx.draw_networkx_labels(G, pos, with_labels=True, font_color="white")
    nx.draw_networkx_edges(G, pos)
    edge_labels = {(u, v): np.round(d["weight"], 2) for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black")
    # print(G)
    # detect_community(G)
    plt.show()