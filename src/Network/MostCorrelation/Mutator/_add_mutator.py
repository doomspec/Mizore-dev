import numpy as np
from ._mutator import Mutator
from Network.MostCorrelation._gene_bank import GeneBank


class AddMutator(Mutator):
    """
    Add mutator
    """

    def can_mutate(self, ga, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            ga: MostCorrelation entity
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return len(chromosome.genes) < len(ga._gene_bank)

    def mutate(self, ga, chromosome):
        """

        Args:
            ga: MostCorrelation entity
            chromosome: target chromosome

        Returns: Mutated Genes

        """
        genes = chromosome.genes.copy()
        original_genes = set()
        [original_genes.add(gene) for gene in genes]
        position = np.random.randint(0, len(genes))
        genes.insert(position, np.random.choice(list(set.difference(GeneBank.genes, original_genes))))
        mutate_prob = 0.2
        if ga._fitness(genes) > chromosome.fitness and np.random.random() > mutate_prob:
            return genes
        return chromosome.genes
