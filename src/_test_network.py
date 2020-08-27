import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
if __name__=="__main__":
    #mi=[[0.0, 0.0538758450985564, 0.02614562320786966, 0.02614562320786966, 0.008245482299012799, 0.007864536298169127, 0.012310588191778209, 0.012310588191778209], [0.0538758450985564, 0.0, 0.02614562320786966, 0.02614562320786966, 0.007864536298169127, 0.008245482299012799, 0.012310588191778209, 0.012310588191778209], [0.02614562320786966, 0.02614562320786966, 0.0, 0.01937679910061013, 1.4832056870604793e-05, 1.4832056870604793e-05, 0.0003230449833626914, 0.0054519507555633034], [0.02614562320786966, 0.02614562320786966, 0.01937679910061013, 0.0, 1.4832056870604793e-05, 1.4832056870604793e-05, 0.0054519507555633034, 0.0003230449833626914], [0.008245482299012799, 0.007864536298169127, 1.4832056870604793e-05, 1.4832056870604793e-05, 0.0, 0.012592316707630283, 7.282117723543535e-06, 7.282117723543535e-06], [0.007864536298169127, 0.008245482299012799, 1.4832056870604793e-05, 1.4832056870604793e-05, 0.012592316707630283, 0.0, 7.282117723543535e-06, 7.282117723543535e-06], [0.012310588191778209, 0.012310588191778209, 0.0003230449833626914, 0.0054519507555633034, 7.282117723543535e-06, 7.282117723543535e-06, 0.0, 0.005779662736367819], [0.012310588191778209, 0.012310588191778209, 0.0054519507555633034, 0.0003230449833626914, 7.282117723543535e-06, 7.282117723543535e-06, 0.005779662736367819, 0.0]]
    mi=[[0.0, 0.021162439190284182, 0.012310588191778209, 0.07292515180218262, 0.020901745997648213, 0.012310987481864308], [0.021162439190284182, 0.0, 0.015340506148096098, 0.020901745997648213, 0.014533197324912712, 0.006273653044042406], [0.012310588191778209, 0.015340506148096098, 0.0, 0.012310987481864308, 0.006273653044042406, 0.005801011165626119], [0.07292515180218262, 0.020901745997648213, 0.012310987481864308, 0.0, 0.021162439190284182, 0.012310588191778209], [0.020901745997648213, 0.014533197324912712, 0.006273653044042406, 0.021162439190284182, 0.0, 0.015340506148096098], [0.012310987481864308, 0.006273653044042406, 0.005801011165626119, 0.012310588191778209, 0.015340506148096098, 0.0]]
    mi=np.array(mi)
    mi*=1e2
    G= nx.Graph(mi)
    zero_edge=[]
    for u, v, d in G.edges(data=True):
        print(u,v,np.round(d["weight"],2))
        if abs(d["weight"])<1e-1:
            zero_edge.append((u,v))
    for u,v in zero_edge:
        G.remove_edge(u,v)
    pos=nx.spring_layout(G,k=0.05,scale=100)
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_labels(G,pos,font_color="white")
    nx.draw_networkx_edges(G,pos)
    edge_labels={(u,v): np.round(d["weight"],2) for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color="black")
    plt.savefig("Untitled.png")
    