from ._task import Task
from ..Blocks import BlockCircuit
from ..Blocks._utilities import get_inner_two_circuit_product
from ..Blocks._sparse_circuit_utilities import get_inner_product_task_on_sparse_circuit


class InnerProductTask(Task):
    """
    The task for evaluate the inner product of the wave function produced by circuit1 and circuit2
    """

    def __init__(self, circuit1: BlockCircuit, circuit2: BlockCircuit, is_sparse=False):
        Task.__init__(self)
        self.circuit1 = circuit1
        self.circuit2 = circuit2
        self.is_sparse = is_sparse

    def run(self):
        if not self.is_sparse:
            res = get_inner_two_circuit_product(self.circuit1, self.circuit2)
        else:
            res = get_inner_product_task_on_sparse_circuit(self.circuit1, self.circuit2)
        return res


class InnerProductTaskSparse(Task):

    def __init__(self, circuit1: BlockCircuit, circuit2: BlockCircuit):
        Task.__init__(self)
        self.circuit1 = circuit1
        self.circuit2 = circuit2

    def run(self):
        res = get_inner_product_task_on_sparse_circuit(self.circuit1, self.circuit2)
        return res
