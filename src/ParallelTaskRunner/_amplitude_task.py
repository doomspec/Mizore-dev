from ._task import Task
from Blocks import BlockCircuit
from Utilities.CircuitEvaluation import evaluate_circuit_amplitudes


class AmplitudeTask(Task):

    def __init__(self, circuit: BlockCircuit, bit_strings):
        Task.__init__(self)
        self.circuit = circuit
        self.bit_strings = bit_strings

    def run(self):
        res = evaluate_circuit_amplitudes(self.circuit.n_qubit, self.circuit.get_fixed_parameter_ansatz(),
                                          self.bit_strings)
        return res
