from ._objective import Objective, CostFunction
from ParameterOptimizer._vqs_utilities import calc_RTE_quality_by_circuit
from Utilities.Tools import qubit_operator2matrix
import numpy as np


class CircuitQualityObjective(Objective):

    def __init__(self, energy_obj, diff, obj_info={}):
        self.hamiltonian = energy_obj.hamiltonian
        self.diff = diff
        self.hamiltonian_square = self.hamiltonian*self.hamiltonian
        self.hamiltonian_square.compress()
        self.n_qubit = energy_obj.n_qubit
        Objective.__init__(self, n_qubit=self.n_qubit)
        self.obj_info = obj_info
        self.obj_info["terminate_cost"] = 0

    def get_cost(self):
        return CircuitQualityCost(self.n_qubit,self.hamiltonian,self.hamiltonian_square, self.diff)


class CircuitQualityCost(CostFunction):
    def __init__(self, n_qubit,hamiltonian, hamiltonian_square, diff):
        self.hamiltonian = hamiltonian
        self.hamiltonian_square = hamiltonian_square
        self.diff = diff
        self.hamiltonian_mat = qubit_operator2matrix(
            n_qubit, hamiltonian)

    def get_cost_obj(self, circuit):
        def obj(parameter):
            return calc_RTE_quality_by_circuit(circuit,self.hamiltonian_mat,self.hamiltonian_square,self.diff)
        return obj

    def get_cost_value(self, circuit):
        quality=calc_RTE_quality_by_circuit(circuit,self.hamiltonian_mat,self.hamiltonian_square,self.diff)
        return quality
