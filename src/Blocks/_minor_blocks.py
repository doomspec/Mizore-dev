from Blocks import Block,BlockCircuit,CompositiveBlock
from Utilities.Operations import apply_global_phase
from math import pi

class GlobalPhaseBlock(Block):

    n_parameter = 1
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = True
    IS_DERIVATIVE_DEFINE = True
    def __init__(self, init_angle=0):
        Block.__init__(self, n_parameter=1)
        self.parameter = [init_angle]

    def get_localized_operator(self, qsubset):
        return GlobalPhaseBlock(self.parameter[0])

    def apply_forward_gate(self, parameter, wavefunction):
        apply_global_phase(wavefunction, parameter[0] + self.parameter[0])
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_global_phase(wavefunction, -(parameter[0] + self.parameter[0]))
        return

    def get_derivative_block(self,para_position):
        return GlobalPhaseBlock(init_angle=self.parameter[0]+pi/2)

    def get_gate_used(self):
        return {}

    def __str__(self):
        info = self.basic_info_string()
        info += "; T=" + str(self.parameter[0])
        return info

from Utilities.Operations import apply_H_gates,apply_CZ_gates

class HadamardBlock(Block):
    n_parameter = 0
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = True

    def __init__(self,qsubset):
        Block.__init__(self, n_parameter=0)
        self.qsubset = qsubset

    def apply_forward_gate(self, parameter, wavefunction):
        apply_H_gates(self.qsubset, wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_H_gates(self.qsubset, wavefunction)
        return

    def get_gate_used(self):
        return {"SingleRotation": len(self.qsubset)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        return info

class CZBlock(Block):
    n_parameter = 0
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = False

    def __init__(self, pairset):
        Block.__init__(self, n_parameter=0)
        self.pairset = pairset

    def apply_forward_gate(self, parameter, wavefunction):
        apply_CZ_gates(self.pairset,wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_CZ_gates(self.pairset,wavefunction)
        return

    def get_gate_used(self):
        return {"CZ":len(self.pairset)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; pairset:" + str(self.pairset)
        return info