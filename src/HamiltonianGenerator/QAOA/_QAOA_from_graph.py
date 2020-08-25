import Networkx as nx
from openfermion.ops import QubitOperator

def get_maxcut_hamiltonian_from_graph(graph):
    hamiltonian = QubitOperator()
    for (i, j, wt) in graph.edges.data('weight'):
        hamiltonian += wt * QubitOperator("Z" + str(i) + " Z" + str(j))

    return hamiltonian

def get_tsp_hamiltonian_from_graph(graph):
    # Here nodes coresponding to cities, s coresponding to step
    hamiltonian = QubitOperator()
    nodes = len(graph.nodes)
    for s in range(nodes):
        for (i, j, wt) in graph.edges.data('weight'):
            hamiltonian += -wt * QubitOperator("Z" + str(i * nodes + s))
            hamiltonian += -wt * QubitOperator("Z" + str(j * nodes + s + 1))
            hamiltonian += wt * QubitOperator("Z" + str(i * nodes + s) +
                                "Z" + str(j * nodes + s + 1))  
    return hamiltonian