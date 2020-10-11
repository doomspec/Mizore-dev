from ._block import Block
from ._block_circuit import BlockCircuit
from ._utilities import get_inverse_circuit


class CompositiveBlock(Block):
    """
    To define a Block by a block circuit
    """
    IS_INVERSE_DEFINED = True

    def __init__(self, circuit: BlockCircuit):
        Block.__init__(self, n_parameter=0)
        self._circuit = circuit
        self.n_parameter = self._circuit.count_n_parameter()
        self.parameter = [0.0] * self.n_parameter

    def apply_forward_gate(self, parameter, wavefunction):
        temp_circuit = self._circuit.duplicate()
        temp_circuit.adjust_all_parameter_by_list(self.parameter)
        temp_circuit.get_ansatz().ansatz(parameter, wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        temp_circuit = self._circuit.duplicate()
        temp_circuit.adjust_all_parameter_by_list(self.parameter)
        get_inverse_circuit(temp_circuit).get_ansatz().ansatz(parameter, wavefunction)
        return

    def __str__(self):
        info = self.basic_info_string()
        return info
