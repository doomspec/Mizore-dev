from ._block_circuit import BlockCircuit
from copy import copy


def concatenate_circuit(first_circuit: BlockCircuit = None, second_circuit: BlockCircuit = None):
    return concatenate_circuit_list((first_circuit, second_circuit))


def concatenate_circuit_list(circuit_list=None):
    n_qubit = circuit_list[0].n_qubit
    new_circuit = BlockCircuit(n_qubit)
    for circuit in circuit_list:
        if circuit.n_qubit != n_qubit:
            raise Exception(
                "The number of qubit of the circuits is not unified!")
        for block in circuit.block_list:
            new_circuit.add_block(copy(block))
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
    from Utilities.CircuitEvaluation import evaluate_circuit_0000_amplitudes

    circuit = concatenate_circuit(
        first_circuit, get_inverse_circuit(second_circuit))

    ansatz = circuit.get_fixed_parameter_ansatz().ansatz
    amp_0000 = evaluate_circuit_0000_amplitudes(first_circuit.n_qubit, ansatz)
    # print(amp_0000,circuit)
    return amp_0000


def get_circuit_energy(circuit, hamiltonian):
    from ParameterOptimizer.ObjWrapper import evaluate_ansatz_expectation
    ansatz = circuit.get_fixed_parameter_ansatz().ansatz
    return evaluate_ansatz_expectation([], circuit.n_qubit, hamiltonian, ansatz)
