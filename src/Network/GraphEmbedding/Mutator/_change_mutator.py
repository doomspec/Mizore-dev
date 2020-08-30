import numpy as np
from ._mutator import Mutator
from minorminer import find_embedding


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
        embedding = find_embedding(ga._graph.edges, ga._target_graph.edges)
        mutated_genes = [(key, value[0]) for key, value in embedding.items()]
        if ga._fitness(mutated_genes) > chromosome.fitness:
            return mutated_genes
        return chromosome.genes
