from ._task import Task
from Blocks import BlockCircuit
from openfermion.ops import QubitOperator
from Objective._objective import CostFunction
from numpy.linalg import norm


class GradientTask(Task):
    """
    The task for evaluate the gradient of a cost function at a point
    The start point should be defined in the input BlockCircuit
    A derivative vector will be returned
    """

    def __init__(self, circuit: BlockCircuit, cost: CostFunction, step_size=1e-6):
        Task.__init__(self)
        self.circuit = circuit
        self.cost = cost
        self.step_size = step_size

    def run(self):
        obj = self.cost.get_cost_obj(self.circuit)
        n_parameter = self.circuit.count_n_parameter_on_active_position()
        x = [0.0] * n_parameter
        init_cost = obj(x)
        cost_list = [0.0] * n_parameter
        for i in range(n_parameter):
            x[i] = self.step_size
            cost_list[i] = (obj(x) - init_cost) / self.step_size
            x[i] = 0.0
        return cost_list
