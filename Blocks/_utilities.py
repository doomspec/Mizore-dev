from Blocks._block_circuit import BlockCircuit
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
