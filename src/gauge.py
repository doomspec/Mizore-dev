import numpy as np

from Utilities.CircuitEvaluation import get_quantum_engine
from projectq.ops import All, Measure
from Blocks import BlockCircuit
from Blocks import HardwareEfficientEntangler, RotationEntangler, HartreeFockInitBlock, SingleParameterMultiRotationEntangler
from ParameterOptimizer import BasinhoppingOptimizer
from Objective import EnergyObjective, AmplitudeObjective
from openfermion.ops import QubitOperator

def get_coverage(bc: BlockCircuit, state_init = '0000', state_j = '1111'): 
    n_qubit = len(state_init)
    init_set = []
    for i, value in enumerate(state_init):
        if value == '1':
            init_set.append(i)

    j_set = []
    for i, value in enumerate(state_j):
        if value == '1':
            j_set.append(i)
            
    coverage = []
    init_block = HartreeFockInitBlock(init_set)
    final_block = HartreeFockInitBlock(j_set)
    obj = AmplitudeObjective(n_qubit)
    for i, block in enumerate(bc.block_list):
        circuit = BlockCircuit(n_qubit)
        circuit.add_block(init_block) 
        for j in range(i+1):
            circuit.add_block(bc.block_list[j])
        circuit.add_block(final_block)
        print(circuit)
        optimizer = BasinhoppingOptimizer(random_initial=0.1) # The initial parameter will be a random value between -0.1 and +0.1
        
        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        coverage.append(- coverage_high - coverage_low)

    return coverage

def get_parameter_efficiency(bc: BlockCircuit, state = '1100'):  #TODO
    n_qubit = len(state)
    qsubset = []
    for i in range(state):
        if state[i] == 1:
            qsubset.append(i)
    efficiency = []

    for i in range(len(bc.block_list)):
        engine = get_quantum_engine()
        wavefunction = engine.allocate_qureg(n_qubit) # Initialize the wavefunction
        engine.flush()
        init = HartreeFockInitBlock(qsubset)
        init.apply([1.0], wavefunction)

        amp_high = []
        amp_low = []
        n_parameter = len(bc.count_n_parameter_by_position_list([n in range(i+1)]))

        optimizer=BasinhoppingOptimizer(random_initial=0.1) # The initial parameter will be a random value between -0.1 and +0.1
        energy, amp = optimizer.run_optimization(bc[i],state_obj.get_cost())

        bc.apply(wavefunction)

        engine.backend.cheat()[1]
        for j in range(len(amp_high)):
            coverage += amp_high[j]*np.conjugate(amp_high[j]) - amp_low[j]*np.conjugate(amp_low[j])

        efficiency.append(coverage / n_parameter) 

    return efficiency

def output_region(bc: BlockCircuit, obj, state = '1100'):  #TODO
    n_qubit = len(state)
    qsubset = []
    for i in range(state):
        if state[i] == 1:
            qsubset.append(i)
    region = []

    for i in range(len(bc.block_list)):
        engine = get_quantum_engine()
        wavefunction = engine.allocate_qureg(n_qubit) # Initialize the wavefunction
        engine.flush()
        init = HartreeFockInitBlock(qsubset)
        init.apply([1.0], wavefunction)

        amp_high = []
        amp_low = []
        n_parameter = len(bc.count_n_parameter_by_position_list([n in range(i+1)]))

        optimizer=BasinhoppingOptimizer(random_initial=0.1) # The initial parameter will be a random value between -0.1 and +0.1
        e_high, amp = optimizer.run_optimization(bc[i], obj.get_cost())

        bc.apply(wavefunction)

        engine.backend.cheat()[1]

        region.append([e_low, e_high]) 

    return region



state_init = '0000'
state_j = '1100'
n_qubit = len(state_init)
bc=BlockCircuit(n_qubit)
bc.add_block(SingleParameterMultiRotationEntangler(0.3*QubitOperator("X" + str(0) + " Y" + str(1))
            +0.5*QubitOperator("X" + str(1) + " Y" + str(2)), init_angle = [0.5]))
#bc.add_block(RotationEntangler((1,2,3),(3,2,1)))

print(bc)
print(get_coverage(bc, state_init, state_j))

