class Chromosome:
    """
    Chromosome for GA
    """

    def __init__(self, genes, max_block_size):
        self.genes = genes
        self.fitness = 0xFFFFFFF
        self.max_block_size = max_block_size
