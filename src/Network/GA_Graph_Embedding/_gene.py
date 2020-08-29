class Gene:
    """
    Wrapper for block
    """

    def __init__(self, entity):
        self.gene = entity

    def __str__(self):
        return f'Gene: {self.gene}'
