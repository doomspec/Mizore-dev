from ._task import Task
from Blocks import BlockCircuit
from Utilities.CircuitEvaluation import evaluate_ansatz_expectation
from collections import Iterable

class ExpectationValueTask(Task):
    """
    The task of expectation value evaluation. If the observable is set to be the Hamiltonian, energy estimation will be evaluated. 
    """
    
    def __init__(self, circuit: BlockCircuit, observable):
        Task.__init__(self)
        self.circuit = circuit
        self.observable = observable

    def run(self):
        if not isinstance(self.observable,Iterable):
            res = evaluate_ansatz_expectation([], self.circuit.n_qubit, self.observable,self.circuit.get_fixed_parameter_ansatz().ansatz)
            return res
        else:
            res=[]
            for o in self.observable:
                e=evaluate_ansatz_expectation([], self.circuit.n_qubit, o,self.circuit.get_fixed_parameter_ansatz().ansatz)
                res.append(e)
            return res