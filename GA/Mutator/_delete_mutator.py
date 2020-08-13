import numpy as np
from ._mutator import Mutator


class DeleteMutator(Mutator):
    """
    Delete mutator
    """

    def can_mutate(self, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return len(chromosome.genes) > 1

    def mutate(self, chromosome):
        """

        Args:
            chromosome: target chromosome

        Returns: Mutated Genes

        """
        genes = chromosome.genes.copy()
        genes.remove(np.random.choice(genes))
        return genes
