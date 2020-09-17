from ._block import Block
from Utilities.Operations import generalized_rotation
from Utilities.Tools import pauliword2string

PAULI_DICT={1:'X',2:'Y',3:'Z'}

class RotationEntangler(Block):
    """Entangler of the form: e^{iPt}
    Attributes:
        qsubset: The subset of qubits in the wave function that the entangler applies on
        pauliword: The Pauli word P in e^{iPt}
        parameter: t in e^{iPt}
    """
    n_parameter = 1
    IS_INVERSE_DEFINED = True
    IS_DERIVATIVE_DEFINE = True

    def __init__(self, qsubset, pauliword, init_angle=0.0):
        Block.__init__(self, n_parameter=1, active_qubits=qsubset)
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

    def get_derivative_block(self,para_position):
        from ._compositive_block import CompositiveBlock
        from ._block_circuit import BlockCircuit
        from ._pauli_gates_block import PauliGatesBlock
        from ._minor_blocks import GlobalPhaseBlock
        from math import pi
        bc=BlockCircuit(0,init_block=self)
        paulistring=[(self.qsubset[i],PAULI_DICT[self.pauliword[i]]) for i in range(len(self.qsubset))]
        #print(paulistring)
        bc.add_block(PauliGatesBlock(paulistring))
        bc.add_block(GlobalPhaseBlock(init_angle=pi/2))
        return CompositiveBlock(bc)

    def get_gate_used(self):
        return {"CNOT": (len(self.qsubset) - 1) * 2,
                "SingleRotation": count_single_gate_for_pauliword(self.pauliword) + 1}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        info += "; Pauli:" + pauliword2string(self.pauliword)
        return info

def count_single_gate_for_pauliword(pauliword):
    n_rotation = 0
    for term in pauliword:
        if term != 3:
            n_rotation += 1
    return n_rotation * 2
