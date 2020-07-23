from ._objective import Objective
from Blocks import HartreeFockInitBlock


class HamiltonianObjective(Objective):
    def __init__(self, hamiltonian, n_qubit, init_block=None, obj_info={}):
        self.hamiltonian = hamiltonian
        self.n_qubit = n_qubit
        self.obj_info = obj_info
        self.init_block = None
        if init_block != None:
            self.init_block = init_block
        else:
            self.init_block = HartreeFockInitBlock([])
        return
