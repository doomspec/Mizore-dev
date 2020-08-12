class Mutator:
    """
    Base class of mutator
    """

    def __init__(self, name):
        self.name = name

    def can_mutate(self, chromosome):
        """
        Check chromosome chould be mutate or not
        Args:
            chromosome: target chromosome for mutation

        Returns: whether chromosome can be mutate

        """
        return False

    def mutate(self, chromosome):
        pass
