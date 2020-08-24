from ._task import Task
from Blocks import BlockCircuit
from Blocks._utilities import get_inner_two_circuit_product


class InnerProductTask(Task):
    
    def __init__(self, circuit1: BlockCircuit, circuit2: BlockCircuit):
        Task.__init__(self)
        self.circuit1 = circuit1
        self.circuit2 = circuit2

    def run(self):
        res = get_inner_two_circuit_product(self.circuit1,self.circuit2)
        return res
