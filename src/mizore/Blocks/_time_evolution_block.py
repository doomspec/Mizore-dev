from ._block import Block
from ..Utilities.Operations import apply_time_evolution
from ..Utilities.Tools import get_operator_qsubset


class TimeEvolutionBlock(Block):
    n_parameter = 1
    IS_INVERSE_DEFINED = True

    def __init__(self, hamiltonian, init_angle=0):
        qsubset = get_operator_qsubset(hamiltonian)
        Block.__init__(self, n_parameter=1, active_qubits=qsubset)
        self.hamiltonian = hamiltonian
        self.parameter = [init_angle]

    def apply_forward_gate(self, parameter, wavefunction):
        apply_time_evolution(self.hamiltonian, parameter[0] + self.parameter[0], wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_time_evolution(self.hamiltonian, -(parameter[0] + self.parameter[0]), wavefunction)
        return

    def get_gate_used(self):
        return {"TimeEvolution": 1}

    def __str__(self):
        info = self.basic_info_string()
        info += "; TimeEvolution: T=" + str(self.parameter[0])
        return info
