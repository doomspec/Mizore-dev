from Benchmark.graph import Graph, generate_graph_node_dict
from Benchmark.MaxCut.util import *


def get_solution_cut_size(solution, graph):
    """Compute the Cut given a partition of the nodes.
    Args:
        solution: list[0,1]
            A list of 0-1 values indicating the partition of the nodes of a graph into two
            separate sets.
        graph: networkx.Graph
            Input graph object.
    """

    if len(solution) != len(graph.nodes):
        raise Exception("trial solution size is {}, which does not match graph size which is {}".format(len(solution),
                                                                                                        len(
                                                                                                            graph.nodes)))

    cut_size = 0
    node_dict = generate_graph_node_dict(graph)
    for edge in graph.edges:
        node_index1 = node_dict[edge.from_node]
        node_index2 = node_dict[edge.to_node]
        if solution[node_index1] != solution[node_index2]:
            cut_size += 1
    return cut_size


def solve_maxcut_by_exhaustive_search(graph):
    """Brute-force solver for MAXCUT instances using exhaustive search.
    Args:
        graph (networkx.Graph): undirected weighted graph describing the MAXCUT
        instance.

    Returns:
        tuple: tuple whose first elements is the number of cuts, and second is a list
            of bit strings that correspond to the solution(s).
    """

    solution_set = []
    num_nodes = len(graph.nodes)

    # find one MAXCUT solution
    maxcut = -1
    one_maxcut_solution = None
    for i in range(0, 2 ** num_nodes):
        trial_solution = dec2bin(i, num_nodes)
        current_cut = get_solution_cut_size(trial_solution, graph)
        if current_cut > maxcut:
            one_maxcut_solution = trial_solution
            maxcut = current_cut
    solution_set.append(one_maxcut_solution)

    # search again to pick up any degeneracies
    for i in range(0, 2 ** num_nodes):
        trial_solution = dec2bin(i, num_nodes)
        current_cut = get_solution_cut_size(trial_solution, graph)
        if current_cut == maxcut and trial_solution != one_maxcut_solution:
            solution_set.append(trial_solution)

    return maxcut, solution_set


def build_graph():
    # build simple test case
    graph = Graph()
    graph.add_edge(1, 2, 1)
    graph.add_edge(1, 3, 1)
    graph.add_edge(2, 3, 1)
    graph.add_edge(2, 4, 1)
    graph.add_edge(3, 5, 1)
    graph.add_edge(4, 5, 1)
    return graph


def main():
    graph = build_graph()
    maxcut, solution_set = solve_maxcut_by_exhaustive_search(graph)
    print (maxcut, solution_set)


if __name__ == '__main__':
    main()
