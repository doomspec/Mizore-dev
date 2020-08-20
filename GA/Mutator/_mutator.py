class Mutator:
    """
    Base class of mutator
    """

    def __init__(self, name):
        self.name = name

    def can_mutate(self, ga, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            ga: ga entity
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return False

    def mutate(self, ga, chromosome):
        pass
