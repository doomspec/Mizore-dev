from scipy.optimize import minimize, basinhopping
from .ObjWrapper import get_obj_for_optimizer
from Utilities.Tools import random_list
from Blocks import BlockCircuit
from ._parameter_optimizer import ParameterOptimizer
from Blocks._utilities import get_inner_two_circuit_product, get_circuit_energy
from scipy import linalg
import numpy
from Utilities.Visulization import draw_x_y_line_relation
NOT_DEFINED = 999999


class ImaginaryTimeEvolutionOptimizer(ParameterOptimizer):
    """
    This class implements imaginary time evolution described in npj Quantum Information (2019) 5:75.
    Differing from the original paper, here we calculate the A and C matrix by finite difference rather than the swap test.
    """

    def __init__(self, random_adjust=0.01, diff=1e-4, stepsize=1e-1, n_step=10, max_increase_n_step=3,
                 task_manager=None, verbose=False, fig_path=None):
        ParameterOptimizer.__init__(self)

        self.random_adjust = random_adjust
        self.stepsize = stepsize
        self.diff = diff
        self.max_increase_n_step = max_increase_n_step
        self.n_step = n_step
        self.verbose = verbose
        self.fig_path = fig_path

    def get_adjusted_circuit(self, circuit):
        adjusted_circuits = []
        diff = self.diff
        for position in circuit.active_position_list:
            block_n_para = circuit.block_list[position].n_parameter
            for in_block_position in range(block_n_para):
                adjust_list = [0.0] * block_n_para
                adjust_list[in_block_position] += diff
                adjusted_circuit = circuit.duplicate()
                adjusted_circuit.adjust_parameter_by_block_postion(
                    adjust_list, position)
                adjusted_circuits.append(adjusted_circuit)
        return adjusted_circuits

    def calc_complex_A_mat(self, circuit, adjusted_circuits):
        n_parameter = len(adjusted_circuits)
        mat_A = [[0.0 for col in range(n_parameter)]
                 for row in range(n_parameter)]
        for i in range(n_parameter):
            for j in range(i, n_parameter):
                inner_product1 = get_inner_two_circuit_product(
                    adjusted_circuits[i], adjusted_circuits[j])
                inner_product2 = get_inner_two_circuit_product(
                    adjusted_circuits[i], circuit)
                inner_product3 = get_inner_two_circuit_product(
                    circuit, adjusted_circuits[j])
                term_value = inner_product1 - inner_product2 - inner_product3 + 1
                term_value /= (self.diff * self.diff)
                term_value = term_value.real
                mat_A[i][j] = term_value
                mat_A[j][i] = term_value
        return mat_A

    def calc_A_mat(self, circuit, adjusted_circuits):
        return numpy.real(self.calc_complex_A_mat(circuit,adjusted_circuits))

    def calc_C_mat(self, circuit, adjusted_circuits,hamiltonian):
        n_parameter = len(adjusted_circuits)
        origin_energy = get_circuit_energy(circuit, hamiltonian)
        mat_C = [0.0 for col in range(n_parameter)]
        for i in range(n_parameter):
            term_value = get_circuit_energy(
                adjusted_circuits[i], hamiltonian) - origin_energy
            term_value /= self.diff
            term_value *= -0.5
            mat_C[i] = term_value
        return mat_C

    def calc_derivative(self, mat_A, mat_C):
        n_parameter = len(mat_C)
        try:
            derivative = linalg.solve(mat_A, mat_C)
        except linalg.LinAlgError:
            derivative = numpy.array(random_list(-self.random_adjust,
                                                 self.random_adjust, n_parameter))

        derivative_norm = linalg.norm(derivative)
        derivative *= self.stepsize / derivative_norm
        return derivative

    def save_fig(self,energy_list):
        if self.fig_path != None:
            draw_x_y_line_relation(list(range(len(energy_list))), energy_list,
                                   "Index of Iteration", "Energy", filename=self.fig_path)

    def run_optimization(self, _circuit: BlockCircuit, cost):
        """
        Carry out ImaginaryTimeEvolution on the active positions of the BlockCircuit provided.
        """
        hamiltonian = cost.hamiltonian
        start_energy = get_circuit_energy(_circuit, hamiltonian)
        lowest_energy = start_energy
        lowest_energy_circuit = _circuit
        energy_list = []
        energy_list.append(start_energy)

        circuit = _circuit.duplicate()
        original_parameter = circuit.get_parameter_on_active_position()

        n_parameter = circuit.count_n_parameter_on_active_position()

        if n_parameter == 0:
            # If active position list is empty, make all the position active
            circuit.active_position_list = list(range(len(circuit.block_list)))
            n_parameter = circuit.count_n_parameter_on_active_position()

        if self.random_adjust != 0:
            random_adjust_list = random_list(-self.random_adjust,
                                             self.random_adjust, n_parameter)
            circuit.adjust_parameter_on_active_position(random_adjust_list)

        previous_energy = lowest_energy
        increase_n_step = 0

        for i in range(0, self.n_step):

            adjusted_circuits = self.get_adjusted_circuit(circuit)
            mat_A = self.calc_A_mat(circuit, adjusted_circuits)
            mat_C = self.calc_C_mat(circuit, adjusted_circuits, hamiltonian)
            derivative = self.calc_derivative(mat_A, mat_C)
            circuit.adjust_parameter_on_active_position(derivative)

            energy = get_circuit_energy(circuit, hamiltonian)
            energy_list.append(energy)
            self.save_fig(energy_list)

            if energy < lowest_energy:
                lowest_energy = energy
                lowest_energy_circuit = circuit
            if energy >= previous_energy:
                increase_n_step += 1
            previous_energy = energy
            if self.verbose:
                print("Lowest History Energy:",
                      lowest_energy, "; Energy Now:", energy)
            if increase_n_step >= self.max_increase_n_step:
                break

        optimal_parameter = lowest_energy_circuit.get_parameter_on_active_position()
        amp = []
        for i in range(len(original_parameter)):
            amp.append(optimal_parameter[i] - original_parameter[i])
        return lowest_energy, amp
