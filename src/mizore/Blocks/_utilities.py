from ._block_circuit import BlockCircuit
from copy import copy
from ..Utilities.CircuitEvaluation import evaluate_ansatz_0000_amplitudes
from ..Utilities.CircuitEvaluation import get_ansatz_complete_amplitudes

def concatenate_circuit(first_circuit: BlockCircuit = None, second_circuit: BlockCircuit = None):
    return concatenate_circuit_list((first_circuit, second_circuit))


def concatenate_circuit_list(circuit_list=None):
    n_qubit = circuit_list[0].n_qubit
    new_active_qubit_list = []
    new_circuit = BlockCircuit(n_qubit)
    for circuit in circuit_list:
        if circuit.n_qubit != n_qubit:
            raise Exception(
                "The number of qubit of the circuits is not unified!")
        n_block_added = len(new_circuit.block_list)
        for active in circuit.active_position_list:
            # print(active,len(new_circuit.block_list))
            new_active_qubit_list.append(active + n_block_added)
        for block in circuit.block_list:
            new_circuit.add_block(copy(block))
        new_circuit.active_position_list = copy(new_active_qubit_list)
    return new_circuit


def get_inverse_circuit(circuit: BlockCircuit):
    new_circuit = BlockCircuit(circuit.n_qubit)
    for block in reversed(circuit.block_list):
        reversed_block = copy(block)
        reversed_block.is_inversed = True
        new_circuit.add_block(reversed_block)
    return new_circuit


def get_inner_two_circuit_product(first_circuit: BlockCircuit, second_circuit: BlockCircuit):
    """
    Return <0...00|circuit(second)^ circuit(first)|0...00>
    """

    circuit = concatenate_circuit(
        first_circuit, get_inverse_circuit(second_circuit))

    ansatz = circuit.get_fixed_parameter_ansatz().ansatz
    amp_0000 = evaluate_ansatz_0000_amplitudes(first_circuit.n_qubit, ansatz)
    # print(amp_0000,circuit)
    return amp_0000


def get_circuit_energy(circuit, hamiltonian):
    from ..ParameterOptimizer.ObjWrapper import evaluate_ansatz_expectation
    ansatz = circuit.get_fixed_parameter_ansatz().ansatz
    return evaluate_ansatz_expectation([], circuit.n_qubit, hamiltonian, ansatz)


def get_0000_amplitude_on_circuit(circuit):
    pcircuit = circuit.get_fixed_parameter_ansatz()
    amp = evaluate_ansatz_0000_amplitudes(pcircuit.n_qubit, pcircuit.ansatz)
    return amp


def get_circuit_complete_amplitudes(circuit):
    pcircuit = circuit.get_fixed_parameter_ansatz()
    amps = get_ansatz_complete_amplitudes(pcircuit.n_qubit, pcircuit.ansatz)
    return amps

def evaluate_off_diagonal_term_by_amps(amp1,amp2,ops_mat):
    import numpy as np
    amp3=np.dot(ops_mat,amp1)
    return np.dot(np.conjugate(amp2),amp3)