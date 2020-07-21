from Objective._objective import Objective
from Blocks._HF_init_operator import HartreeFockInitOperator
class HamiltonianObjective(Objective):
    hamiltonian=None
    n_qubit=0
    init_block=None
    def __init__(self,hamiltonian,n_qubit,init_operator=None):
        self.hamiltonian=hamiltonian
        self.n_qubit=n_qubit
        if init_operator!=None:
            self.init_operator=init_operator
        else:
            self.init_block=HartreeFockInitBlock((,))
        return