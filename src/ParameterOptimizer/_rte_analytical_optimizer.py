from ._real_time_evolution_optimizer import *
from Utilities.Tools import qubit_operator2matrix, random_list
from Blocks._utilities import get_circuit_complete_amplitudes, evaluate_off_diagonal_term_by_amps, get_circuit_energy, get_inner_two_circuit_product


class RTEAnalyticalOptimizer(RealTimeEvolutionOptimizer):
    def __init__(self, *args, **kwargs):
        RealTimeEvolutionOptimizer.__init__(self, *args, **kwargs)

    def calc_derivative(self, circuit, hamiltonian, hamiltonian_square=None):
        derivative_circuits = get_derivative_circuit(circuit)
        mat_C = np.imag(self.calc_C_mat(
            circuit, derivative_circuits, hamiltonian))
        mat_A = np.real(self.calc_A_mat(circuit, derivative_circuits))
        try:
            derivative = linalg.solve(mat_A, mat_C)
        except linalg.LinAlgError:
            n_parameter = len(derivative_circuits)
            derivative = np.array(random_list(-self.random_adjust,
                                              self.random_adjust, n_parameter))
        if hamiltonian_square is not None:
            quality=self.calc_quality(mat_A, mat_C, derivative, hamiltonian_square, circuit)
            return derivative,quality
        else:
            return derivative

    def calc_A_mat(self, circuit, derivative_circuits):
        if self.task_manager == None:
            return calc_A_mat_analytical_0(circuit, derivative_circuits)
        else:
            return calc_A_mat_analytical_parallel(self.task_manager, circuit, derivative_circuits)

    def calc_C_mat(self, circuit, derivative_circuits, hamiltonian):
        if self.hamiltonian_mat is None:
            self.hamiltonian_mat = qubit_operator2matrix(
                circuit.n_qubit, hamiltonian)
        return calc_C_mat_by_hamiltonian_mat_analytical(self.hamiltonian_mat, circuit, derivative_circuits)
