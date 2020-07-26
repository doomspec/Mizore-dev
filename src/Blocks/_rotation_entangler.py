from ._block import Block
from Utilities.Operations import generalized_rotation
from Utilities.Tools import pauliword2string


class RotationEntangler(Block):
    """Entangler of the form: e^{iPt}
    Attributes:
        qsubset: The subset of qubits in the wavefunction that the entangler applies on
        pauliword: The Pauli word P in e^{iPt}
        parameter: t in e^{iPt}
    """
    n_parameter = 1
    IS_INVERSE_DEFINED = True

    def __init__(self, qsubset, pauliword, init_angle=0.0):
        Block.__init__(self, n_parameter=1)
        self.pauliword = pauliword
        self.parameter = [init_angle]
        self.qsubset = qsubset

    def apply_forward_gate(self, parameter, wavefunction):
        generalized_rotation(wavefunction, self.qsubset,
                             self.pauliword, evolution_time=parameter[0] + self.parameter[0])
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        generalized_rotation(wavefunction, self.qsubset,
                             self.pauliword, evolution_time=-(parameter[0] + self.parameter[0]))
        return

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        info += "; Pauli:" + pauliword2string(self.pauliword)
        return info
