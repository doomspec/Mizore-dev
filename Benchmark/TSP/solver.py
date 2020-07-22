import random
import itertools
from Benchmark.graph import Graph
from Benchmark.node import Node


def sim_annealing(cities, start, epoch=5000):
    # This function uses sim_annealing which creates random paths and checks if the previous path is shorter than the old path.
    # Simulated annealing: http://katrinaeg.com/simulated-annealing.html
    for i in range(epoch):
        best_tot_dist = None
        best_path = None
        path, tot_dist = gen_rand_path(cities, start)

        # If first run then var is None and first value is equal to best value
        if (best_tot_dist == None):
            best_tot_dist = tot_dist
            best_path = path

        # Else check if current best distane is higher than total distance of function.
        elif (best_tot_dist > tot_dist):
            best_path = path
            best_tot_dist = tot_dist

    return best_path, best_tot_dist


def gen_rand_path(cities, start):
    # Generate random solution
    current_city = start
    path = [start]
    tot_dist = 0

    while len(cities) > (len(path)):
        # Set previous city to determine total distance from previous city to new city.
        prev_city = current_city

        # Get random pick for city that is not already in path
        current_city = random.choice([a for a in current_city.neighbors if a not in path])

        # Calculate total distance
        tot_dist += prev_city.find_weight(current_city)

        # Append current city to path
        path.append(current_city)

    return path, tot_dist


def brute_force(cities, start):
    min_dis = 0xFFFFFFFFFFFFF
    min_path = []

    # calculate cost
    def calculate_path_cost(path=[]):
        cost = 0
        for i in range(len(path) - 1):
            cur_city = path[i]
            next_city = path[i + 1]
            # valid path
            if not cur_city.has_neighbor(next_city):
                return 0xFFFFFFFFFFFFF
            cost += cur_city.find_weight(next_city)
        return cost

    # brute force iteration
    for path in itertools.permutations(cities):
        if path[0] != start:
            continue
        # calculate cost
        cost = calculate_path_cost(path)
        if min_dis > cost:
            min_dis = cost
            min_path = path
    return min_path, min_dis


def build_cities():
    # simple test case
    graph = Graph()
    graph.add_edge("RV", "UL", 86)
    graph.add_edge("UL", "RV", 86)
    graph.add_edge('RV', 'S', 195)
    graph.add_edge('S', 'RV', 195)
    graph.add_edge('RV', 'M', 178)
    graph.add_edge('M', 'RV', 178)
    graph.add_edge("UL", "S", 107)
    graph.add_edge("S", "UL", 107)
    graph.add_edge("UL", "M", 123)
    graph.add_edge("M", "UL", 123)
    graph.add_edge("S", "M", 230)
    graph.add_edge("M", "S", 230)
    return graph


def main():
    graph = build_cities()
    cities = list(graph.nodes)
    start = random.choice(cities)
    short_route_sa, tot_dist_sa = sim_annealing(cities, start)
    short_route_bf, tot_dist_bf = brute_force(cities, start)

    if (tot_dist_sa > tot_dist_bf):
        short_route = short_route_bf
        tot_dist = tot_dist_bf
        best_func = brute_force.__name__

    else:
        short_route = short_route_sa
        tot_dist = tot_dist_sa
        best_func = sim_annealing.__name__

    print('Shortest route: ' + str(" -> ".join([a.name for a in short_route])) + '. Total distance: ' + str(tot_dist)
          + '. Best function : ' + best_func)


if __name__ == '__main__':
    main()
