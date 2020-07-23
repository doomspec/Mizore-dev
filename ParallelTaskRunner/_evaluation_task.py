from ._task import Task
from Blocks import BlockCircuit
from openfermion.ops import QubitOperator
from Utilities.CircuitEvaluation import evaluate_circuit_energy


class EvaluationTask(Task):
    
    def __init__(self, circuit: BlockCircuit, hamiltonian):
        Task.__init__(self)
        self.circuit = circuit
        self.hamiltonian = hamiltonian

    def run(self):
        res = evaluate_circuit_energy([],self.circuit.n_qubit,self.circuit.get_fixed_parameter_ansatz(),self.bit_strings)
        return res
