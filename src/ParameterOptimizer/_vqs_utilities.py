from Blocks._utilities import get_circuit_complete_amplitudes, evaluate_off_diagonal_term_by_amps, get_circuit_energy, get_inner_two_circuit_product
import numpy as np
import time
from ParallelTaskRunner._inner_product_task import InnerProductTask
LARGE_NUMBER = 99999

def calc_RTE_quality_by_circuit(circuit, hamiltonian_mat, hamiltonian_square, diff):

    adjusted_circuits = get_adjusted_circuit(diff, circuit)
    mat_B = calc_B_mat(circuit, adjusted_circuits)
    mat_C = np.imag(calc_C_mat_by_hamiltonian_mat(
        hamiltonian_mat, diff, circuit, adjusted_circuits))
    mat_A = np.real(calc_A_mat_0(
        diff, circuit, adjusted_circuits, mat_B))
    try:
        derivative = np.linalg.solve(mat_A, mat_C)
    except np.linalg.LinAlgError:
        return LARGE_NUMBER
    quality = calc_RTE_quality(
        hamiltonian_square, mat_A, mat_C, derivative, circuit)
    return abs(quality)


def calc_RTE_quality_by_circuit_analytical(circuit, hamiltonian_mat, hamiltonian_square):

    derivative_circuits = get_derivative_circuit(circuit)
    mat_C = np.imag(calc_C_mat_by_hamiltonian_mat_analytical(
        hamiltonian_mat, circuit, derivative_circuits))
    mat_A = np.real(calc_A_mat_analytical_0(circuit, derivative_circuits))
    derivative=calc_derivative(mat_A,mat_C)
    quality = calc_RTE_quality(
        hamiltonian_square, mat_A, mat_C, derivative, circuit)
    return abs(quality)

def calc_derivative(mat_A,mat_C):
    try:
        return np.linalg.solve(mat_A, mat_C)
    except np.linalg.LinAlgError:
        return [LARGE_NUMBER]*len(mat_C)

def calc_quality_derivative_by_obj_parallel_ana(task_manager,quality_cost,circuit):
    derivative_circuits=get_derivative_circuit(circuit)
    return calc_derivative_quality_parallel_ana(task_manager,quality_cost.hamiltonian_mat,quality_cost.hamiltonian_square,circuit,derivative_circuits)

def calc_derivative_quality_parallel_ana(task_manager,hamiltonian_mat,hamiltonian_square,circuit,derivative_circuits):
    mat_C,mat_A=calc_mat_C_A_parallel_ana(task_manager,hamiltonian_mat,circuit,derivative_circuits)
    derivative=calc_derivative(mat_A,mat_C)
    quality = calc_RTE_quality(
        hamiltonian_square, mat_A, mat_C, derivative, circuit)
    return derivative,quality

def calc_mat_C_A_parallel_ana(task_manager,hamiltonian_mat,circuit,derivative_circuits):
    mat_C_id=add_calc_C_mat_analytical_task(task_manager,hamiltonian_mat,circuit,derivative_circuits)
    task_manager.flush(task_package_size=1)
    mat_A_id=add_calc_A_mat_analytical_tasks(task_manager,circuit,derivative_circuits)
    task_manager.flush(task_package_size=20)
    mat_C=task_manager.receive_task_result(task_series_id=mat_C_id)[0]
    mat_A=calc_A_mat_analytical_by_task_results(task_manager,mat_A_id,len(derivative_circuits))
    return mat_C,mat_A
    

def calc_RTE_quality(hamiltonian_square, mat_A, mat_C, derivative, circuit):
    n_parameter = len(mat_C)
    quality = 0
    for i in range(n_parameter):
        for j in range(n_parameter):
            quality += mat_A[i][j]*derivative[i]*derivative[j]
    for i in range(n_parameter):
        quality -= 2*mat_C[i]*derivative[i]
    quality += get_circuit_energy(circuit, hamiltonian_square)
    if quality < -1e-1:
        print(quality)
        print(derivative)
    return abs(quality)

def get_derivative_circuit(circuit):
    derivative_circuits = []
    for position in circuit.active_position_list:
        active_block = circuit.block_list[position]
        block_n_para = active_block.n_parameter
        for in_block_position in range(block_n_para):
            derivative_block = active_block.get_derivative_block(
                in_block_position)
            derivative_circuit = circuit.duplicate()
            derivative_circuit.block_list[position] = derivative_block
            derivative_circuits.append(derivative_circuit)
    return derivative_circuits


def get_adjusted_circuit(diff, circuit):
    adjusted_circuits = []
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


def calc_real_C_mat(diff, circuit, adjusted_circuits, hamiltonian):
    n_parameter = len(adjusted_circuits)
    origin_energy = get_circuit_energy(circuit, hamiltonian)
    mat_C = np.array([0.0 for col in range(n_parameter)])
    for i in range(n_parameter):
        term_value = get_circuit_energy(
            adjusted_circuits[i], hamiltonian) - origin_energy
        term_value /= diff
        term_value *= 0.5
        mat_C[i] = term_value
    return mat_C

def calc_C_mat_by_hamiltonian_mat_analytical(hamiltonian_mat, circuit, derivative_circuits):
    n_parameter = len(derivative_circuits)
    derivative_circuit_amps = [get_circuit_complete_amplitudes(
        derivative_circuit) for derivative_circuit in derivative_circuits]
    circuit_amp = get_circuit_complete_amplitudes(circuit)
    mat_C = np.array([0.0 for col in range(n_parameter)], dtype=complex)
    for i in range(n_parameter):
        term_value = evaluate_off_diagonal_term_by_amps(
            circuit_amp, derivative_circuit_amps[i], hamiltonian_mat)
        mat_C[i] = term_value
    return mat_C

def add_calc_C_mat_analytical_task(task_manager,hamiltonian_mat, circuit, derivative_circuits):
    task=MatCTask(hamiltonian_mat, circuit, derivative_circuits)
    task_id_i = "mat_C_calc"+ str(time.time() % 10000)
    task_manager.add_task_to_buffer(task, task_series_id=task_id_i)
    return task_id_i

from ParallelTaskRunner._task import Task
class MatCTask(Task):
    def __init__(self, hamiltonian_mat, circuit, derivative_circuits):
        Task.__init__(self)
        self.circuit = circuit
        self.hamiltonian_mat = hamiltonian_mat
        self.derivative_circuits = derivative_circuits
    def run(self):
        return calc_C_mat_by_hamiltonian_mat_analytical(self.hamiltonian_mat, self.circuit, self.derivative_circuits)

def calc_C_mat_by_hamiltonian_mat(hamiltonian_mat, diff, circuit, adjusted_circuits):
    adjusted_circuit_amps = [get_circuit_complete_amplitudes(
        adjusted_circuit) for adjusted_circuit in adjusted_circuits]
    circuit_amp = get_circuit_complete_amplitudes(circuit)
    mat_C = np.array([0.0 for col in range(
        len(adjusted_circuits))], dtype=complex)
    origin_energy = np.dot(np.conjugate(circuit_amp),
                           np.dot(hamiltonian_mat, circuit_amp))
    for i in range(len(adjusted_circuits)):
        term_value = evaluate_off_diagonal_term_by_amps(
            circuit_amp, adjusted_circuit_amps[i], hamiltonian_mat)-origin_energy
        term_value /= diff
        mat_C[i] = term_value
    return mat_C


def calc_A_mat_analytical_0(circuit, derivative_circuits):
    n_parameter = len(derivative_circuits)
    mat_A = np.array([[0.0 for col in range(n_parameter)]
                      for row in range(n_parameter)], dtype=complex)
    for i in range(n_parameter):
        for j in range(i, n_parameter):
            inner_product1 = get_inner_two_circuit_product(
                derivative_circuits[j], derivative_circuits[i])
            mat_A[i][j] = inner_product1
            mat_A[j][i] = np.conjugate(inner_product1)
    return mat_A

def add_calc_A_mat_analytical_tasks(task_manager, circuit, derivative_circuits):
    n_parameter = len(derivative_circuits)
    task_id_i = "mat_A_calc"+ str(time.time() % 10000)
    for i in range(n_parameter):
        for j in range(i+1, n_parameter):
            task_manager.add_task_to_buffer(InnerProductTask(
                derivative_circuits[j], derivative_circuits[i]), task_series_id=task_id_i)
    return task_id_i

def calc_A_mat_analytical_by_task_results(task_manager, task_id_i, n_parameter):
    inner_product_list = task_manager.receive_task_result(task_series_id=task_id_i)
    mat_A = np.eye(n_parameter,dtype=complex)
    inner_index=0
    for i in range(n_parameter):
        for j in range(i+1, n_parameter):
            inner_product=inner_product_list[inner_index]
            inner_index+=1
            mat_A[i][j] = inner_product
            mat_A[j][i] = np.conjugate(inner_product)
    return mat_A


def calc_A_mat_analytical_parallel(task_manager, circuit, derivative_circuits,min_n_task=20):
    n_parameter = len(derivative_circuits)
    task_id_i=add_calc_A_mat_analytical_tasks(task_manager,circuit,derivative_circuits)
    n_task=task_manager.n_task_remain_by_series_id[task_id_i]
    task_manager.flush(task_package_size=max(min_n_task,(n_task//task_manager.n_processor)+1))
    mat_A=calc_A_mat_analytical_by_task_results(task_manager,task_id_i,n_parameter)
    return mat_A


def calc_A_mat_analytical_parallel_old(task_manager, circuit, derivative_circuits):
    n_parameter = len(derivative_circuits)
    mat_A = np.array([[0.0 for col in range(n_parameter)]
                      for row in range(n_parameter)], dtype=complex)
    
    task_id_i = "mat_A_calc"+ str(time.time() % 100000)
    n_task=0
    for i in range(n_parameter):
        for j in range(i+1, n_parameter):
            task_manager.add_task_to_buffer(InnerProductTask(
                derivative_circuits[j], derivative_circuits[i]), task_series_id=task_id_i)
            n_task+=1
    task_manager.flush(task_package_size=max(20,(n_task//task_manager.n_processor)+1))
    inner_product_list = task_manager.receive_task_result(task_series_id=task_id_i)
    inner_index=0
    mat_A = np.eye(n_parameter,dtype=complex)
    for i in range(n_parameter):
        for j in range(i+1, n_parameter):
            inner_product=inner_product_list[inner_index]
            inner_index+=1
            mat_A[i][j] = inner_product
            mat_A[j][i] = np.conjugate(inner_product)
    return mat_A


def calc_A_mat_0(diff, circuit, adjusted_circuits, mat_B):
    n_parameter = len(adjusted_circuits)
    mat_A = np.array([[0.0 for col in range(n_parameter)]
                      for row in range(n_parameter)], dtype=complex)
    for i in range(n_parameter):
        for j in range(i, n_parameter):
            inner_product1 = get_inner_two_circuit_product(
                adjusted_circuits[j], adjusted_circuits[i])
            term_value = inner_product1 - np.conjugate(mat_B[j]) - mat_B[i] + 1
            term_value /= (diff * diff)
            mat_A[i][j] = term_value
            mat_A[j][i] = np.conjugate(term_value)
    return mat_A


def calc_A_mat_parallel(task_manager, diff, circuit, adjusted_circuits, mat_B):
    n_parameter = len(adjusted_circuits)
    mat_A = np.array([[0.0 for col in range(n_parameter)]
                      for row in range(n_parameter)], dtype=complex)
    task_id_i = "mat_A_calc"+ str(time.time() % 100000)

    for i in range(n_parameter):
        for j in range(i, n_parameter):
            task_manager.add_task_to_buffer(InnerProductTask(
                adjusted_circuits[i], adjusted_circuits[j]), task_series_id=task_id_i)
    task_manager.flush()
    inner_product_list = task_manager.receive_task_result(task_series_id=task_id_i)
    inner_index=0
    for i in range(n_parameter):
        for j in range(i, n_parameter):
            inner_product=inner_product_list[inner_index]
            inner_index+=1
            term_value = inner_product - \
                np.conjugate(mat_B[i]) - mat_B[j] + 1
            term_value /= (diff * diff)
            mat_A[i][j] = term_value
            mat_A[j][i] = np.conjugate(term_value)
    return mat_A


def calc_B_mat(circuit, adjusted_circuits):
    mat_B = [get_inner_two_circuit_product(
        circuit, adjusted_circuits[i]) for i in range(len(adjusted_circuits))]
    return mat_B


def calc_M_mat(mat_A, mat_B):
    n_parameter = len(mat_B)
    mat_M = [[0.0 for col in range(n_parameter)]
             for row in range(n_parameter)]
    for i in range(n_parameter):
        for j in range(i, n_parameter):
            mat_M[i][j] = np.real(mat_A[i][j])+mat_B[i]*mat_B[j]
            mat_M[j][i] = mat_M[i][j]
    return mat_M


def calc_V_mat(mat_C, mat_B, current_energy):
    n_parameter = len(mat_B)
    mat_V = np.array([0.0 for col in range(n_parameter)], dtype=complex)
    for i in range(n_parameter):
        mat_V[i] = np.imag(mat_C[i])+1j*current_energy*mat_B[i]
    return mat_V
