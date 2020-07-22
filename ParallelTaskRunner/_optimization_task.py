from ._task import Task
from Blocks import BlockCircuit
from ParameterOptimizer import ParameterOptimizer
from openfermion.ops import QubitOperator


class OptimizationTask(Task):
    
    def __init__(self, circuit: BlockCircuit, optimizer: ParameterOptimizer, hamiltonian: QubitOperator):
        Task.__init__(self)
        self.circuit = circuit
        self.optimizer = optimizer
        self.hamiltonian = hamiltonian

    def run(self):
        pcircuit = self.circuit.get_ansatz_on_active_position()
        res = self.optimizer.run_optimization(pcircuit, self.hamiltonian)
        return res
