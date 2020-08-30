from ._task import Task
from Blocks import BlockCircuit
from Utilities.CircuitEvaluation import evaluate_ansatz_amplitudes


class AmplitudeTask(Task):
    """
    The task of evaluating a amplitude of the wave function produced by a BlockCircuit
    Attributes:
        bit_strings: a list of strings like [[1000],[0110]]. The result of run will be the amplitude of these strings.
    """

    def __init__(self, circuit: BlockCircuit, bit_strings):
        Task.__init__(self)
        self.circuit = circuit
        self.bit_strings = bit_strings

    def run(self):
        res = evaluate_ansatz_amplitudes(self.circuit.n_qubit, self.circuit.get_fixed_parameter_ansatz().ansatz,
                                         self.bit_strings)
        return res
