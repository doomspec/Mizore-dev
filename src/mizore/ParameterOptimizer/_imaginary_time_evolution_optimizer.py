from scipy.optimize import minimize, basinhopping
from .ObjWrapper import get_obj_for_optimizer
from ..Utilities.Tools import random_list
from ..Blocks import BlockCircuit
from ._parameter_optimizer import ParameterOptimizer
from ..Blocks._utilities import get_inner_two_circuit_product, get_circuit_energy
from scipy import linalg
import numpy as np
from ..ParallelTaskRunner import TaskManager
from ..ParallelTaskRunner._inner_product_task import InnerProductTask
from ..Utilities.Visulization import draw_x_y_line_relation
from ._vqs_utilities import *


NOT_DEFINED = 999999


class ImaginaryTimeEvolutionOptimizer(ParameterOptimizer):
    """
    This class implements imaginary time evolution described in npj Quantum Information (2019) 5:75.
    Differing from the original paper, here we calculate the A and C matrix by finite difference rather than the swap test.
    """

    def __init__(self, get_best_result=True, random_adjust=0.01, diff=1e-4, stepsize=1e-1, n_step=10,
                 max_increase_n_step=3,
                 inverse_evolution=False, task_manager: TaskManager = None, calculate_quality=False, verbose=False, fig_path=None):
        ParameterOptimizer.__init__(self)

        self.get_best_result = get_best_result
        self.random_adjust = random_adjust
        self.stepsize = stepsize
        self.diff = diff
        self.max_increase_n_step = max_increase_n_step
        self.n_step = n_step
        self.inverse_evolution = inverse_evolution
        self.verbose = verbose
        self.fig_path = fig_path
        self.task_manager = task_manager
        self.calculate_quality = calculate_quality
        if calculate_quality:
            self.hamiltonian_square = None

    def save_fig(self, energy_list):
        if self.fig_path == None:
            return
        if self.fig_path == "screen":

            draw_x_y_line_relation(list(range(len(energy_list))), energy_list,
                                   "Index of Iteration", "Energy", filename=None)
        else:
            draw_x_y_line_relation(list(range(len(energy_list))), energy_list,
                                   "Index of Iteration", "Energy", filename=self.fig_path)

    def calc_A_mat(self, circuit, adjusted_circuits, mat_B):
        if self.task_manager == None:
            return calc_A_mat_0(self.diff, circuit, adjusted_circuits, mat_B)
        else:
            return calc_A_mat_parallel(self.task_manager, self.diff, circuit, adjusted_circuits, mat_B)

    def calc_C_mat(self, circuit, adjusted_circuits, hamiltonian):
        return calc_real_C_mat(self.diff, circuit, adjusted_circuits, hamiltonian)

    def calc_derivative(self, circuit, hamiltonian):

        adjusted_circuits = get_adjusted_circuit(self.diff, circuit)
        n_parameter = len(adjusted_circuits)
        mat_B = calc_B_mat(circuit, adjusted_circuits)
        mat_C = (-1)*self.calc_C_mat(circuit, adjusted_circuits, hamiltonian)
        mat_A = np.real(self.calc_A_mat(circuit, adjusted_circuits, mat_B))
        try:
            derivative = linalg.solve(mat_A, mat_C)
        except linalg.LinAlgError:
            derivative = np.array(random_list(-self.random_adjust,
                                              self.random_adjust, n_parameter))
        if self.calculate_quality:
            print("Quality", self.calc_quality(
                mat_A, mat_C, derivative, circuit))
        return derivative

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

            derivative = self.calc_derivative(circuit, hamiltonian)
            if derivative is None:
                break
            derivative_norm = linalg.norm(derivative)
            para_shift = derivative * self.stepsize / derivative_norm
            if self.inverse_evolution:
                para_shift = -1 * para_shift
            circuit.adjust_parameter_on_active_position(para_shift)
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

        if self.get_best_result:
            optimal_parameter = lowest_energy_circuit.get_parameter_on_active_position()
            res_energy = lowest_energy
        else:
            optimal_parameter = circuit.get_parameter_on_active_position()
            res_energy = energy_list[len(energy_list) - 1]

        amp = []
        for i in range(len(original_parameter)):
            amp.append(optimal_parameter[i] - original_parameter[i])
        return res_energy, amp

    def calc_quality(self, mat_A, mat_C, derivative, circuit):
        return "Not defined for ITE"
