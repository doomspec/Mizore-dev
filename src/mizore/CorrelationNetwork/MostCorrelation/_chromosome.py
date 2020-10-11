class Chromosome:
    """
    Chromosome for MostCorrelation
    """

    def __init__(self, genes):
        self.genes = genes
        self.fitness = -0xFFFFFFF

    def __iter__(self):
        return iter(self.genes)
