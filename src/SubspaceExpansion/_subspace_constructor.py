from Blocks import BlockCircuit, HartreeFockInitBlock
from Blocks._time_evolution_block import TimeEvolutionBlock
import itertools
from collections import Iterable
from ._krylov_algorithm import generate_krylov_circuits
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init


def init_res_circuit_list(circuits):
    if not isinstance(circuits, Iterable):
        res_circuits = [circuits.duplicate()]
    else:
        res_circuits = [circuit.duplicate() for circuit in circuits]
    return res_circuits


def add_local_krylov_basis(circuits, qsubset, energy_obj, delta_t, n_circuit):
    res_circuits = init_res_circuit_list(circuits)

    local_hamiltonian = get_reduced_energy_obj_with_HF_init(
        energy_obj, None, location2keep=qsubset, relabel_qubits=False).hamiltonian
    for circuit in circuits:
        res_circuits.extend(generate_krylov_circuits(
            circuit, local_hamiltonian, delta_t, n_circuit))

    return res_circuits


def add_local_complete_basis(circuits, qsubset):
    res_circuits = init_res_circuit_list(circuits)
    
    n_qubit = len(qsubset)
    for circuit in circuits:
        for l in range(1, n_qubit+1):
            for qset0 in itertools.combinations(qsubset, l):
                temp_circuit = circuit.duplicate()
                temp_circuit.add_block(HartreeFockInitBlock(qset0))
                res_circuits.append(temp_circuit)

    return res_circuits
