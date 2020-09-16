from Blocks._utilities import get_circuit_complete_amplitudes, evaluate_off_diagonal_term_by_amps, get_circuit_energy, get_inner_two_circuit_product
import numpy as np
import time
from ParallelTaskRunner._inner_product_task import InnerProductTask



def calc_RTE_quality_by_circuit(circuit, hamiltonian_mat, hamiltonian_square, diff):
    
    LARGE_NUMBER=99999
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
        hamiltonian_mat, mat_A, mat_C, derivative, circuit)
    return quality


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

def calc_RTE_quality1(hamiltonian_mat, mat_A, mat_C, derivative, circuit):
    n_parameter = len(mat_C)
    
    part1=0
    for i in range(n_parameter):
        for j in range(n_parameter):
            part1 += mat_A[i][j]*derivative[i]*derivative[j]
    part2=0
    for i in range(n_parameter):
        part2 -= 2*mat_C[i]*derivative[i]
    circuit_amp = get_circuit_complete_amplitudes(circuit)
    amp3 = np.dot(hamiltonian_mat,circuit_amp)
    part3= np.real(np.dot(np.conjugate(amp3),amp3))
    quality = part1+part2+part3
    if quality<-1e-4:
        print(quality)
        print(derivative)
        print(part1,part2,part3)
    if quality<0:
        return quality
    return quality


def calc_RTE_quality(hamiltonian_square, mat_A, mat_C, derivative, circuit):
    n_parameter = len(mat_C)
    quality = 0
    for i in range(n_parameter):
        for j in range(n_parameter):
            quality += mat_A[i][j]*derivative[i]*derivative[j]
    for i in range(n_parameter):
        quality -= 2*mat_C[i]*derivative[i]
    quality += get_circuit_energy(circuit, hamiltonian_square)
    if quality<-1e-1:
        print(quality)
        print(derivative)
    return quality


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
    task_id = id(time.time()) % 10000
    for i in range(n_parameter):
        for j in range(i, n_parameter):
            task_id_i = str(task_id) + "i" + str(i)
            task_manager.add_task_to_buffer(InnerProductTask(
                adjusted_circuits[i], adjusted_circuits[j]), task_series_id=task_id_i + "inner")
    task_manager.flush()
    for i in range(n_parameter):
        task_id_i = str(task_id) + "i" + str(i)
        inner_product_list1 = task_manager.receive_task_result(
            task_series_id=task_id_i + "inner")
        for j in range(i, n_parameter):
            term_value = inner_product_list1[j - i] - \
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
