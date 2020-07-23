from Blocks import Block
from Utilities.Operations import apply_X_gates


class HartreeFockInitBlock(Block):
    """Apply X gates on a few of qubits. Usually for getting Hartree-Fock qubit wavefunction
    Attributes:
        qsubset: should be the qubits where X gates to be applied
    """
    n_parameter = 0
    IS_INVERSE_DEFINED = True

    def __init__(self, qsubset, init_angle=0):
        Block.__init__(self, n_parameter=0)
        self.qsubset = qsubset

    def apply_forward_gate(self, parameter, wavefunction):
        apply_X_gates(self.qsubset, wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_X_gates(self.qsubset, wavefunction)
        return

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        return info
