import itertools
import numpy as np


def _fitness(_graph, genes=[]):
    edges = itertools.combinations(genes, 2)
    node_num = len(genes)
    fitness = np.sum([_graph[item[0]][item[1]]["weight"] for item in edges]) / (
            (node_num - 1) * node_num)
    return fitness


def _brute_force(g, num=10):
    node = g.nodes
    max_val = -1
    for i in range(2, num + 1):
        combs = itertools.combinations(node, i)
        for item in combs:
            fit = _fitness(g, item)
            if max_val < fit:
                max_val = fit
    print(max_val)
