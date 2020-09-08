from Blocks import BlockCircuit
from Blocks._time_evolution_block import TimeEvolutionBlock
from Utilities.Tools import get_operator_n_qubit


def generate_krylov_circuits(init_circuit: BlockCircuit, hamiltonian, delta_t, n_circuit):
    """
    Generate Block Circuits who produce a Krylov basis as described in 
    "A multireference quantum krylov algorithm for strongly correlated electrons"
    (J.C.T.C 2020, 16, 4, 2236–2245)
    Args:
        The states are like {e^{i *delta_t* n}|*init_circuit*> | n in 0,1,...,*n_circuit*}
    """

    circuits = [0] * n_circuit

    for i in range(1, n_circuit + 1):
        circuit = init_circuit.duplicate()
        circuit.add_block(TimeEvolutionBlock(hamiltonian, init_angle=delta_t * i))
        circuits[i - 1] = circuit
        # print(circuit)
    return circuits
