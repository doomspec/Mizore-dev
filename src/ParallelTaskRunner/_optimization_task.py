from ._task import Task
from Blocks import BlockCircuit
from ParameterOptimizer import ParameterOptimizer
from openfermion.ops import QubitOperator
from Objective._objective import CostFunction
class OptimizationTask(Task):

    def __init__(self, circuit: BlockCircuit, optimizer: ParameterOptimizer, cost:CostFunction):
        Task.__init__(self)
        self.circuit = circuit
        self.optimizer = optimizer
        self.cost = cost

    def run(self):
        res = self.optimizer.run_optimization(self.circuit, self.cost)
        return res
