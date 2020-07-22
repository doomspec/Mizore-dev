from scipy.optimize import minimize, basinhopping
from ParameterOptimizer.ObjWrapper import get_obj_for_optimizer
from Utilities.Tools import random_list
#from Blocks import BlockCircuit
from ParameterOptimizer import ParameterOptimizer
from Blocks._utilities import get_inner_two_circuit_product, get_circuit_energy
from scipy import linalg


class ImaginaryTimeEvolutionOptimizer(ParameterOptimizer):

    def __init__(self, random_initial=0.01, diff=1e-4, stepsize=1e-1, tol=1e-6, max_acceptable_increase_n_step=10):
        ParameterOptimizer.__init__(self)

        self.random_initial = random_initial
        self.stepsize = stepsize
        self.diff = diff
        self.tol = tol

    def run_optimization(self, _circuit, hamiltonian):

        circuit=_circuit.duplicate()
        n_parameter = circuit.get_active_n_parameter()

        initial_parameter = [0.0]*n_parameter

        if self.random_initial != 0:
            initial_parameter = random_list(-self.random_initial,
                                            self.random_initial, n_parameter)
            for i in range(n_parameter):
                circuit.adjust_parameter_by_postion(initial_parameter[i], i)

        print(circuit)
        print(get_circuit_energy(circuit, hamiltonian))

        for i in range(0, 10):

            mat_A = [[0.0 for col in range(n_parameter)]
                     for row in range(n_parameter)]
            mat_C = [0.0 for col in range(n_parameter)]

            adjusted_circuits = [None for col in range(n_parameter)]

            diff = self.diff

            # adjusted_circuit=circuit.duplicate()
            # adjusted_circuit.adjust_parameter_by_postion(diff,1)
            # adjusted_circuits[1]=adjusted_circuit

            for i in range(n_parameter):
                adjusted_circuit = circuit.duplicate()
                adjusted_circuit.adjust_parameter_by_postion(diff, i)
                adjusted_circuits[i] = adjusted_circuit
                # print(adjusted_circuit)

            for i in range(n_parameter):
                for j in range(i, n_parameter):
                    inner_product1 = get_inner_two_circuit_product(
                        adjusted_circuits[i], adjusted_circuits[j])
                    inner_product2 = get_inner_two_circuit_product(
                        adjusted_circuits[i], circuit)
                    inner_product3 = get_inner_two_circuit_product(
                        circuit, adjusted_circuits[j])
                    term_value = inner_product1-inner_product2-inner_product3+1
                    term_value /= diff*diff
                    term_value = term_value.real
                    mat_A[i][j] = term_value
                    mat_A[j][i] = term_value

            # print(mat_A)

            origin_energy = get_circuit_energy(circuit, hamiltonian)
            for i in range(n_parameter):
                term_value = get_circuit_energy(
                    adjusted_circuits[i], hamiltonian)-origin_energy
                term_value /= diff
                term_value *= -0.5
                mat_C[i] = term_value

            # print(mat_C)
            try:
                ITE_derivative = linalg.solve(mat_A, mat_C)
            except linalg.LinAlgError:
                ITE_derivative = random_list(-self.random_initial,
                                            self.random_initial, n_parameter)

            ITE_derivative /= linalg.norm(ITE_derivative)
            ITE_derivative *= self.stepsize

            # print(ITE_derivative)
            circuit.adjust_parameter_by_list(ITE_derivative)
            print(circuit)
            print(get_circuit_energy(circuit, hamiltonian))
