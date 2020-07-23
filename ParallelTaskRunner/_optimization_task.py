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
        res = self.optimizer.run_optimization(self.circuit, self.hamiltonian)
        return res
