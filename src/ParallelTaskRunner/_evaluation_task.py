from ._task import Task
from Blocks import BlockCircuit
from Utilities.CircuitEvaluation import evaluate_ansatz_expectation


class ExpectationValueTask(Task):
    
    def __init__(self, circuit: BlockCircuit, observable):
        Task.__init__(self)
        self.circuit = circuit
        self.observable = observable

    def run(self):
        res = evaluate_ansatz_expectation([], self.circuit.n_qubit, self.observable,self.circuit.get_fixed_parameter_ansatz())
        return res
