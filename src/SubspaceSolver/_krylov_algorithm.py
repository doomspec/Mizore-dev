from Blocks import BlockCircuit
from Blocks._time_evolution_block import TimeEvolutionBlock
from Blocks._trotter_evolution_block import TrotterTimeEvolutionBlock
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
    return circuits

def generate_trotter_krylov_circuits(init_circuit: BlockCircuit, hamiltonian, delta_t,n_trotter_step, n_circuit, use_total_trotter_step=False):
    """
    if use_total_trotter_step is True, n_trotter_step will be regarded as the trotter step number of every step
    if not, in every delta_t, n_trotter_step repetitions of 1 step trotter will be used
    """
    circuits = [0] * n_circuit
    
    for i in range(1, n_circuit + 1):
        circuit = init_circuit.duplicate()
        if not use_total_trotter_step:
            circuit.add_block(TrotterTimeEvolutionBlock(hamiltonian,n_trotter_step=n_trotter_step* i,evolution_time=delta_t * i))
        else:
            circuit.add_block(TrotterTimeEvolutionBlock(hamiltonian,n_trotter_step=n_trotter_step,evolution_time=delta_t * i))
        circuits[i - 1] = circuit
    return circuits