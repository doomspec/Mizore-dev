from ._gene_bank import GeneBank
from ._gene import Gene
from ._chromosome import Chromosome
from .Mutator._change_mutator import ChangeMutator
import networkx as nx
import numpy as np
import logging
import time
import copy
import itertools
from minorminer import find_embedding

logger = logging.getLogger(__name__)


class GAGraphEmbeddingConstructor:
    """
    MostCorrelation Constructor for the circuit
    """

    def __init__(self, graph: nx.Graph, target_graph: nx.Graph, initial_gene_size=4, max_chromosome_size=10,
                 verbose=False):
        self._graph = graph
        self.verbose = verbose
        self._target_graph = target_graph
        self._chromosomes = self._init_chromosomes(max_chromosome_size, initial_gene_size)
        self._mutators = self._init_mutators()
        for c in self._chromosomes:
            self._fitness(c.genes)
        # note that result is a list of best individual in each iteration
        self.result = []

    def _init_chromosomes(self, max_chromosome_size, initial_gene_size):
        """
        Initial  chromosomes
        Args:
            max_chromosome_size: max size of genes can be loaded into chromosome
            size: size of chromosomes

        Returns: Generated chromosomes

        """
        chromosomes = []
        for i in range(max_chromosome_size):
            embedding = find_embedding(self._graph.edges, self._target_graph.edges)
            genes = [(key, value[0]) for key, value in embedding.items()]
            chromosomes.append(Chromosome(genes))
        return chromosomes

    def _init_mutators(self):
        """

        Returns: mutator for evolution

        """
        mutators = list()
        mutators.append(ChangeMutator("Change mutator"))
        return mutators

    def run(self, time_budget=0, iteration=0):
        """
        Main loop for MostCorrelation
        Args:
            time_budget: time for computation
            iteration: max iteration time

        Returns: best result

        """
        counter = 0
        start_time = time.time()
        while (time_budget != 0 and start_time + time_budget > time.time()) or (iteration != 0 and counter < iteration):
            self._chromosomes = self._evolve(self._chromosomes)
            for chromosome in self._chromosomes:
                self.result.append(copy.deepcopy(chromosome))

            if self.verbose:
                print(
                    f'time: {time.time()}, round:{counter}, best result:{sorted(self._chromosomes, key=lambda x: x.fitness)[0].fitness}')
            counter += 1
        return self.result

    def _evolve(self, chromosomes=[]):
        """
        iteration evolving
        Args:
            chromosomes: population

        Returns: generated chromosomes

        """
        for chromosome in chromosomes:
            chromosome.fitness = self._fitness(chromosome.genes)
        chromosomes = self._selection(chromosomes)
        chromosomes = self._crossover(chromosomes)
        self._mutation(chromosomes)
        for chromosome in chromosomes:
            chromosome.fitness = self._fitness(chromosome.genes)
        return chromosomes

    def _fitness(self, genes=[]):
        """
        Fitness function for chromosomes
        Args:
            chromosomes: current population

        Returns: calculated chromosomes

        """
        embedding_map = {}
        fitness = 0
        for item in genes:
            embedding_map[item[0]] = item[1]

        for edge in self._graph.edges:
            try:
                fitness += self._graph[edge[0]][edge[1]]["weight"] * \
                           self._target_graph[embedding_map[edge[0]]][embedding_map[edge[1]]]["weight"]
            except:
                pass
        return fitness

    def _mutation(self, chromosomes=[]):
        """
        Apply mutation for chromosomes
        Args:
            chromosomes: chromosomes in current evolution

        Returns: mutated chromosomes

        """
        mutation_prob = 0.6
        for chromosome in chromosomes:
            if np.random.random() < mutation_prob:
                applied_mutators = []
                for mutator in self._mutators:
                    if mutator.can_mutate(self, chromosome):
                        applied_mutators.append(mutator)
                if len(applied_mutators) == 0:
                    continue
                mutator = np.random.choice(applied_mutators)
                chromosome.genes = mutator.mutate(self, chromosome)

    def _selection(self, chromosomes=[]):
        """
        Since there is no strategies for selection
        Args:
            chromosomes: current chromosomes

        Returns: selection of chromosomes

        """
        return chromosomes

    def _crossover(self, chromosomes=[]):
        """

        Args:
            chromosomes: list of chromosomes

        Returns: chromosomes after crossover

        """
        father = chromosomes[:len(chromosomes) // 2]
        mother = chromosomes[len(chromosomes) // 2:]
        crossover_range = min(len(father), len(mother))
        crossover_prob = 0.8
        new_population = []
        for i in range(crossover_range):
            if np.random.rand() < crossover_prob:
                son = mother[i]
                daughter = father[i]
            else:
                daughter = mother[i]
                son = father[i]
            new_population.append(son)
            new_population.append(daughter)
        # check if not even
        if len(chromosomes) % 2 == 1:
            rest = chromosomes[crossover_range << 1:]
            if np.random.rand() < 0.5:
                new_population.extend(rest)
            else:
                rest.extend(new_population)
                new_population = rest
        return new_population

    def get_result(self):
        """

        Returns: rest of MostCorrelation

        """
        iter_set = set()
        res = []
        for chromosome in self.result:
            elem = tuple(sorted(chromosome))
            if iter_set.__contains__(elem):
                continue
            res.append(chromosome)
            iter_set.add(elem)
        res = sorted(res, key=lambda x: -x.fitness)
        return res
