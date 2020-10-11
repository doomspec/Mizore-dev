from ._objective import Objective, CostFunction
from ..Blocks._utilities import get_circuit_energy
from openfermion.ops import QubitOperator



class LeastSquareObjective(Objective):
    """
    cost function is defined by |f(x)-<x|H|x>|^2, if H is not specified, default to be all Z measurement
    Attributes:
        function:
        hamiltonian:
        obj_info: The dict for additional information of the Hamiltonian, e.g. the HF energy and the ground state energy
    Methods:
        get_cost(): generate an EnergyCost object which can be used by optimizers
    """

    def __init__(self, function, n_qubit, hamiltonian=None, init_block=None, obj_info={}):
        
        self.function = function
        self.n_qubit = n_qubit
        self.obj_info = obj_info
        if init_block != None:
            self.init_block = init_block
        else:
            self.init_block = HartreeFockInitBlock([])
        if hamiltonian = None:
            self.hamiltonian = QubitOperator()
            for i in range(n_qubit):
            self.hamiltonian += QubitOperator("Z"+str(i))
        else:
            self.hamiltonian = hamiltonian
        return

    def get_cost(self):
        return EnergyCost(self.function, self.hamiltonian)


from ..Utilities.CircuitEvaluation import evaluate_ansatz_expectation


class EnergyCost(CostFunction):
    def __init__(self, function, hamiltonian):
        self.function = function
        self.hamiltonian = hamiltonian

    def get_cost_obj(self, circuit):
        pcircuit = circuit.get_ansatz_on_active_position()

        def obj(parameter):
            exp = evaluate_ansatz_expectation(parameter, pcircuit.n_qubit, self.hamiltonian, pcircuit.ansatz)
            distance = (self.function - exp)**2
            return distance

        return obj

    def get_cost_value(self, circuit):
        pcircuit = circuit.get_fixed_parameter_ansatz()
        exp = evaluate_ansatz_expectation([], pcircuit.n_qubit, self.hamiltonian, pcircuit.ansatz)
        distance = (self.function - exp)**2
        return distance
