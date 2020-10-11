from ._objective import Objective, CostFunction
from ..Blocks import HartreeFockInitBlock
from ..Blocks._utilities import get_circuit_energy


class EnergyObjective(Objective):
    """
    Attributes:
        Hamiltonian
        init_block: the block usually used for initiate the wave fucntion for the Hamiltonian.
        A block that produce a state near the ground state should be adopted.
        Usually, for the molecule, the Hartree Fock initialization is used
        obj_info: The dict for additional information of the Hamiltonian, e.g. the HF energy and the ground state energy
    Methods:
        get_cost(): generate a EnergyCost object which can be used by optimizers
    """

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

    def get_cost(self):
        return EnergyCost(self.hamiltonian)


from ..Utilities.CircuitEvaluation import evaluate_ansatz_expectation


class EnergyCost(CostFunction):
    def __init__(self, hamiltonian):
        self.hamiltonian = hamiltonian

    def get_cost_obj(self, circuit):
        pcircuit = circuit.get_ansatz_on_active_position()

        def obj(parameter):
            return evaluate_ansatz_expectation(parameter, pcircuit.n_qubit, self.hamiltonian, pcircuit.ansatz)

        return obj

    def get_cost_value(self, circuit):
        pcircuit = circuit.get_fixed_parameter_ansatz()
        return evaluate_ansatz_expectation([], pcircuit.n_qubit, self.hamiltonian, pcircuit.ansatz)
