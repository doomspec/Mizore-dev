from Blocks import BlockCircuit,HartreeFockInitBlock
from Blocks._time_evolution_block import TimeEvolutionBlock
import itertools



def generate_local_complete_space(circuits,qsubset):
    res_circuits=[circuit.duplicate() for circuit in circuits]
    n_qubit=len(qsubset)

    for circuit in circuits:
        for l in range(1,n_qubit+1):
            for qset0 in itertools.combinations(qsubset,l):
                temp_circuit=circuit.duplicate()
                temp_circuit.add_block(HartreeFockInitBlock(qset0))
                res_circuits.append(temp_circuit)
                
    return res_circuits



