from ._gene_bank import GeneBank
from ._gene import Gene
from ._chromosome import Chromosome
from .Mutator._add_mutator import AddMutator
from .Mutator._delete_mutator import DeleteMutator
from .Mutator._change_mutator import ChangeMutator
import numpy as np
import logging
import time
import copy

logger = logging.getLogger(__name__)


class GAConstructor:
    """
    GA Constructor for the circuit
    """

    def __init__(self, max_block_size=4, max_chromosome_size=5):
        # add identical block to gene bank
        self._gene_bank = list(self._build_gene_bank())
        self._chromosomes = self._init_chromosomes(max_chromosome_size, max_block_size)
        self._mutators = self._init_mutators()
        # note that result is a list of best individual in each iteration
        self.result = Chromosome([], max_block_size)

    def _build_gene_bank(self):
        """
        Build bank of gene

        Returns: genes

        """
        gene_bank = GeneBank()
        gene_bank.genes.add(Gene("1"))
        gene_bank.genes.add(Gene("2"))
        gene_bank.genes.add(Gene("3"))
        gene_bank.genes.add(Gene("4"))
        return gene_bank.genes

    def _init_chromosomes(self, max_chromosome_size, size):
        """
        Initial  chromosomes
        Args:
            max_chromosome_size: max size of genes can be loaded into chromosome
            size: size of chromosomes

        Returns: Generated chromosomes

        """
        chromosomes = []
        for i in range(max_chromosome_size):
            chromosome_len = np.random.randint(1, size + 1)
            genes = list(np.random.choice(self._gene_bank, size=chromosome_len))
            chromosomes.append(Chromosome(genes, size))
        return chromosomes

    def _init_mutators(self):
        """

        Returns: mutator for evolution

        """
        mutators = list()
        mutators.append(AddMutator("Add mutator"))
        mutators.append(DeleteMutator("Delete mutator"))
        mutators.append(ChangeMutator("Change mutator"))
        return mutators

    def run(self, time_budget=0, iteration=0):
        """
        Main loop for GA
        Args:
            time_budget: time for computation
            iteration: max iteration time

        Returns: best result

        """
        counter = 0
        start_time = time.time()
        while (time_budget != 0 and start_time + time_budget > time.time()) or (iteration != 0 and counter < iteration):
            best_individual, self._chromosomes = self._evolve(self._chromosomes)
            if self.result.fitness > best_individual.fitness:
                self.result = copy.deepcopy(best_individual)
            counter += 1
        return self.result

    def _evolve(self, chromosomes=[]):
        """
        iteration evolving
        Args:
            chromosomes: population

        Returns: best individual, generated chromosomes

        """
        self._fitness(chromosomes)
        best_individual = min(chromosomes, key=lambda x: x.fitness)
        chromosomes = self._selection(chromosomes)
        chromosomes = self._crossover(chromosomes)
        self._mutation(chromosomes)
        return best_individual, chromosomes

    def _fitness(self, chromosomes=[]):
        """
        Fitness function for chromosomes
        Args:
            chromosomes: current population

        Returns: calculated chromosomes

        """
        for chromosome in chromosomes:
            chromosome.fitness = np.random.random()

    def _mutation(self, chromosomes=[]):
        """
        Apply mutation for chromosomes
        Args:
            chromosomes: chromosomes in current evolution

        Returns: mutated chromosomes

        """
        mutation_prob = 1
        for chromosome in chromosomes:
            if np.random.random() < mutation_prob:
                applied_mutators = []
                for mutator in self._mutators:
                    if mutator.can_mutate(chromosome):
                        applied_mutators.append(mutator)
                mutator = np.random.choice(applied_mutators)
                chromosome.genes = mutator.mutate(chromosome)

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
