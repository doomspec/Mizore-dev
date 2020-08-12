import numpy as np
from ._mutator import Mutator
from GA._gene_bank import GeneBank


class ChangeMutator(Mutator):
    """
    Change mutator
    """

    def can_mutate(self, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return True

    def mutate(self, chromosome):
        """

        Args:
            chromosome: target chromosome

        Returns: Mutated Genes

        """
        genes = chromosome.genes.copy()
        position = np.random.randint(0, len(genes))
        genes[position] = np.random.choice(list(GeneBank.genes))
        return genes
