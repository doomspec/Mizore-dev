class Block():
    """
    Base class of all the blocks
    A block is a piece of parameterized circuit which achieves certain operation.
    The users may override the methods apply_forward_gate() and apply_inverse_gate()
    to define a new block.

    Blocks may be used in a BlockCircuit or a BlockPool.

    Attributes:
        parameter: The list of parameters of the parametric block
        is_inversed: If true, the function apply() will apply apply_inverse_gate() when called
        IS_INVERSE_DEFINED: Set to be true when apply_inverse_gate() is implemented
    """

    IS_INVERSE_DEFINED = False
    IS_LOCALIZE_AVAILABLE = False

    def __init__(self, is_inversed=False, n_parameter=-1,active_qubits=None):
        self.is_inversed = is_inversed
        self.parameter = []
        self.n_parameter = n_parameter
        self.active_qubits = None
        if active_qubits!=None:
            self.active_qubits = set(active_qubits)
        else:
            self.active_qubits = set()
        return
    
    def get_localized_operator(self,qsubset):
        return None

    def get_active_qubits(self):
        if self.IS_LOCALIZE_AVAILABLE:
            return []
        else:
            return self.active_qubits

    def apply(self, parameter, wavefunction):
        """
        Apply gates parametrized by parameter on the wave function
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

    def adjust_parameter(self, adjuct_list):
        if len(adjuct_list) != len(self.parameter):
            raise Exception("The number of parameter do not match the block!")
        for i in range(len(adjuct_list)):
            self.parameter[i] += adjuct_list[i]

    def __or__(self, wavefunction):
        return

    def basic_info_string(self):
        info = "Type:" + self.__class__.__name__ + "; Para Num:" + str(self.n_parameter)
        if self.is_inversed:
            info += "; INVERSED"
        return info

    def get_gate_used(self):
        return dict()

    def __str__(self):
        return self.basic_info_string()

    def __hash__(self):
        return self.__str__().__hash__()
