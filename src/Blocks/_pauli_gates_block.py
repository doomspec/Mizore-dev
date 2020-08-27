from ._block import Block
from Utilities.Operations import apply_Pauli_gates


class PauliGatesBlock(Block):


    n_parameter = 0
    IS_INVERSE_DEFINED = True

    def __init__(self, paulistring, init_angle=0):
        """
        paulistring should be like [(0,"X"),(2,"Y")]
        """
        Block.__init__(self, n_parameter=0)
        self.paulistring = paulistring
        qsubset=[]

    def apply_forward_gate(self, parameter, wavefunction):
        apply_Pauli_gates(self.paulistring, wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_Pauli_gates(self.paulistring, wavefunction)
        return

    def get_gate_used(self):
        return {"SingleRotation":len(self.paulistring)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; PauliString:" + str(self.paulistring)
        return info
