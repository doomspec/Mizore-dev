import numpy as np
from ._mutator import Mutator
from Network.MostCorrelation._gene_bank import GeneBank


class ChangeMutator(Mutator):
    """
    Change mutator
    """

    def can_mutate(self, ga, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return True

    def mutate(self, ga, chromosome):
        """

        Args:
            chromosome: target chromosome

        Returns: Mutated Genes

        """
        genes = chromosome.genes.copy()
        original_genes = set()
        [original_genes.add(gene) for gene in genes]
        position = np.random.randint(0, len(genes))
        diff_set = set.difference(GeneBank.genes, original_genes)
        if len(diff_set) == 0:
            return genes
        genes[position] = np.random.choice(list(diff_set))
        mutate_prob = 0.2
        if ga._fitness(genes) > chromosome.fitness and np.random.random() > mutate_prob:
            return genes
        return chromosome.genes
