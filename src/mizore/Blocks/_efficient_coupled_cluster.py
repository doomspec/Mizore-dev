from ._block import Block
from ..Utilities.Operations import generalized_rotation, XY_full_rotation, inversed_XY_full_rotation
from ..Utilities.Tools import pauliword2string


class EfficientCoupledCluster(Block):
    """

    """
    n_parameter = -1
    IS_INVERSE_DEFINED = True

    def __init__(self, qsubset, init_angle=None):
        n_parameter = len(qsubset) * 2 + 1
        Block.__init__(self, n_parameter=n_parameter, active_qubits=qsubset)
        self.qsubset = qsubset
        if init_angle == None:
            self.parameter = [0.0] * n_parameter
        else:
            self.parameter = init_angle

    def apply_forward_gate(self, parameter, wavefunction):
        XY_full_rotation(wavefunction, self.qsubset, [
            self.parameter[i] + parameter[i] for i in range(1, len(self.parameter))])
        generalized_rotation(wavefunction, self.qsubset,
                             [1] * len(self.qsubset), evolution_time=parameter[0] + self.parameter[0])
        inversed_XY_full_rotation(wavefunction, self.qsubset, [
            self.parameter[i] + parameter[i] for i in range(1, len(self.parameter))])
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        XY_full_rotation(wavefunction, self.qsubset, [
            self.parameter[i] + parameter[i] for i in range(1, len(self.parameter))])
        generalized_rotation(wavefunction, self.qsubset,
                             [1] * len(self.qsubset), evolution_time=-(parameter[0] + self.parameter[0]))
        inversed_XY_full_rotation(wavefunction, self.qsubset, [
            self.parameter[i] + parameter[i] for i in range(1, len(self.parameter))])
        return

    def get_gate_used(self):
        return {"CNOT": len(self.qsubset) * 2, "SingleRotation": len(self.qsubset) * 2 + 1}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        return info
