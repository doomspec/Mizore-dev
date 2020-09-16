from ._block import Block
from Utilities.Operations import apply_global_phase

class GlobalPhaseBlock(Block):

    n_parameter = 1
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = True

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

    def get_gate_used(self):
        return {}

    def __str__(self):
        info = self.basic_info_string()
        info += "; T=" + str(self.parameter[0])
        return info
