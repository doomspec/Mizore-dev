import numpy as np

from Utilities.CircuitEvaluation import get_quantum_engine
from projectq.ops import All, Measure
from Blocks import BlockCircuit
from Blocks import HardwareEfficientEntangler, RotationEntangler, HartreeFockInitBlock, SingleParameterMultiRotationEntangler
from ParameterOptimizer import BasinhoppingOptimizer
from Objective import EnergyObjective, AmplitudeObjective
from openfermion.ops import QubitOperator
from Benchmark.MaxCut.util import dec2bin
from HamiltonianGenerator import make_example_H2

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
        optimizer = BasinhoppingOptimizer(random_initial=0.1) # The initial parameter will be a random value between -0.1 and +0.1
        
        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        coverage.append(- coverage_high - coverage_low)

    return coverage

def get_parameter_efficiency(bc: BlockCircuit, state_init = '0000'): 
    n_qubit = len(state_init)
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []
    
    for i, block in enumerate(bc.block_list):
        n_parameter.append(block.n_parameter)

    for j in range(pow(2, n_qubit)):
        state = dec2bin(j, n_qubit)
        state_j = ''
        for value in state:
            state_j += str(value)
        """ print(state_j)
        break """
        coverage = get_coverage(bc, state_init, state_j) #list of coverage
        for i, block in enumerate(bc.block_list):
            efficiency[i] += coverage[i] / n_parameter[i]

    return efficiency

def output_region(bc: BlockCircuit, obj, state_init = '0000'):  
    n_qubit = len(state_init)
    efficiency = [0.0 for i in range(len(bc.block_list))]

    for i, block in enumerate(bc.block_list):
        circuit = BlockCircuit(n_qubit)
        circuit.add_block(init_block) 
        for j in range(i+1):
            circuit.add_block(bc.block_list[j])

        optimizer = BasinhoppingOptimizer(random_initial=0.1) # The initial parameter will be a random value between -0.1 and +0.1
        
        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        region.append(- coverage_high - coverage_low)

    return region



state_init = '0000'
state_j = '1100'
n_qubit = len(state_init)
bc=BlockCircuit(n_qubit)
bc.add_block(SingleParameterMultiRotationEntangler(0.3*QubitOperator("X" + str(0) + " Y" + str(1))
            +0.5*QubitOperator("X" + str(1) + " Y" + str(2)), init_angle = [0.5]))
bc.add_block(RotationEntangler((1,2,3),(3,2,1)))
print(bc)

print(get_coverage(bc, state_init, state_j))

#print(get_parameter_efficiency(bc, state_init))

#energy_obj = make_example_H2()
#print(output_region(bc,energy_obj,state_init))
