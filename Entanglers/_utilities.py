from Entanglers._entangler_circuit import EntanglerCircuit
from copy import copy


def concatenate_circuit(first_circuit: EntanglerCircuit = None, second_circuit: EntanglerCircuit = None):
    return concatenate_circuit_list((first_circuit, second_circuit))


def concatenate_circuit_list(circuit_list=None):
    n_qubit = circuit_list[0].n_qubit
    new_circuit = EntanglerCircuit(n_qubit)
    for circuit in circuit_list:
        if circuit.n_qubit != n_qubit:
            raise Exception(
                "The number of qubit of the circuits is not unified!")
        for entangler in circuit.entangler_list:
            new_circuit.add_entangler(copy(entangler))
    return new_circuit


def get_inverse_circuit(circuit: EntanglerCircuit):
    new_circuit = EntanglerCircuit(circuit.n_qubit)
    for entangler in reversed(circuit.entangler_list):
        reversed_entangler = copy(entangler)
        reversed_entangler.is_inversed = True
        new_circuit.add_entangler(reversed_entangler)
    return new_circuit
