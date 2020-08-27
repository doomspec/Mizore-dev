from Blocks import BlockCircuit
from Blocks._time_evolution_block import TimeEvolutionBlock
from Utilities.Tools import get_operator_n_qubit

def generate_Krylov_circuits(hamiltonian,delta_t,n_circuit,init_circuit=None):
    """
    Generate Block Circuits who produce a Krylov basis as described in 
    "A multireference quantum krylov algorithm for strongly correlated electrons"
    (J.C.T.C 2020, 16, 4, 2236–2245)
    Args:
        The states are like {e^{i *delta_t* n}|*init_circuit*> | n in 0,1,...,*n_circuit*}
    """

    n_qubit=get_operator_n_qubit(hamiltonian)
    circuits=[0]*n_circuit
    for i in range(n_circuit):
        circuit=BlockCircuit(n_qubit)
        circuit.add_block(init_circuit)
        circuit.add_block(TimeEvolutionBlock(hamiltonian,init_angle=delta_t*i))
        circuits[i]=circuit
        print(circuit)
    return circuits