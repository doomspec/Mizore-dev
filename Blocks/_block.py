class Block():
    """Base class of all the blocks
    
    Attributes:
        parameter: The list of parameters of the parametried block
        is_inversed: If true, the function apply() will apply apply_inverse_gate() when called
        IS_INVERSE_DEFINED: Set to be true when apply_inverse_gate() is implemented
    """

    IS_INVERSE_DEFINED = False

    def __init__(self, is_inversed=False, n_parameter=-1):
        self.is_inversed = is_inversed
        self.parameter = []
        self.n_parameter = n_parameter
        return

    def apply(self, parameter, wavefunction):
        """
        Apply gates parametrized by parameter on the wavefunction
        """
        if not self.is_inversed:
            self.apply_forward_gate(parameter, wavefunction)
        else:
            self.apply_inverse_gate(parameter, wavefunction)
        return

    def apply_forward_gate(self, parameter, wavefunction):
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        # If there is not inverse operation set, use forward operation as inverse.
        self.apply_forward_gate(parameter, wavefunction)
        return

    def __or__(self, wavefunction):
        return

    def basic_info_string(self):
        info = "Type:" + self.__class__.__name__ + "; Para Num:" + str(self.n_parameter)
        if self.is_inversed:
            info += "; INVERSED"
        return info

    def __str__(self):
        return self.basic_info_string()

    def __hash__(self):
        return self.__str__().__hash__()
