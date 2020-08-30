import numpy as np
from ._mutator import Mutator


class DeleteMutator(Mutator):
    """
    Delete mutator
    """

    def can_mutate(self, ga, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return len(chromosome.genes) > 2

    def mutate(self, ga, chromosome):
        """

        Args:
            chromosome: target chromosome

        Returns: Mutated Genes

        """
        genes = chromosome.genes.copy()
        genes.remove(np.random.choice(genes))
        mutate_prob = 0.2
        if ga._fitness(genes) > chromosome.fitness and np.random.random() > mutate_prob:
            return genes
        return chromosome.genes
