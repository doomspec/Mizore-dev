import numpy as np
from projectq.ops import All, Measure
from openfermion.ops import QubitOperator

from mizore.Utilities.CircuitEvaluation import get_quantum_engine, evaluate_ansatz_1DMs, evaluate_ansatz_2DMs
from mizore.Blocks import BlockCircuit
from mizore.Blocks import HardwareEfficientEntangler, RotationEntangler, HartreeFockInitBlock, \
    SingleParameterMultiRotationEntangler
from mizore.ParameterOptimizer import BasinhoppingOptimizer
from mizore.Objective import EnergyObjective, AmplitudeObjective, OneDMObjective, TwoDMObjective
from mizore.Benchmark.MaxCut.util import dec2bin
from mizore.HamiltonianGenerator import make_example_H2

def get_coverage_one(bc: BlockCircuit, state_init='0000', qubit=0, state=0):
    n_qubit = len(state_init)
    if qubit > n_qubit - 1:
        raise ValueError('qubit shoud be valid index of qubits')
    if state > 2:
        raise ValueError('state shoud be 0 or 1')

    init_set = []
    for i, value in enumerate(state_init):
        if value == '1':
            init_set.append(i)

    coverage = []
    init_block = HartreeFockInitBlock(init_set)
    optimizer = BasinhoppingOptimizer(random_initial=0.1)
    obj = OneDMObjective(n_qubit, qubit, state)
    for i, block in enumerate(bc.block_list):
        circuit = BlockCircuit(n_qubit)
        circuit.add_block(init_block)
        for j in range(i + 1):
            circuit.add_block(bc.block_list[j])
        
        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        coverage.append(- np.real(coverage_high) - np.real(coverage_low))

    return coverage

def get_full_coverage_one(bc: BlockCircuit, n_qubit):
    normalize = 2*n_qubit
    efficiency = [0.0 for i in range(len(bc.block_list))]

    for position, block in enumerate(bc.block_list):
        coverage_high = [0.0 for i in range(normalize)]
        coverage_low = [1.0 for i in range(normalize)]
        for j in range(pow(2, n_qubit)):
            state_init = dec2bin(j, n_qubit)
            init_set = [] 
            for k, value in enumerate(state_init):
                if value == 1:
                    init_set.append(k)    
            
            init_block = HartreeFockInitBlock(init_set)
            circuit = BlockCircuit(n_qubit)
            circuit.add_block(init_block)
            for l in range(position + 1):
                circuit.add_block(bc.block_list[l])
            pcircuit = circuit.get_fixed_parameter_ansatz()

            OneDM = evaluate_ansatz_1DMs([], pcircuit.n_qubit, pcircuit.ansatz)
            for qubit in range(n_qubit):
                for state in range(2):
                    coverage = np.real(OneDM[qubit][state][state]) 
                    if coverage > coverage_high[2*qubit+state]:
                        coverage_high[2*qubit+state] = coverage
                    if coverage < coverage_low[2*qubit+state]:
                        coverage_low[2*qubit+state] = coverage
        
        efficiency[position] = (sum(coverage_high) - sum(coverage_low)) / normalize

    return efficiency

def get_gate_efficiency_one(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 2*n_qubit
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        gates = block.get_gate_used()
        print(gates)
        n_parameter.append(2*gates['CNOT']+gates["SingleRotation"])
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for qubit in range(n_qubit):
        for state in range(2):
            coverage = get_coverage_one(bc, state_init, qubit, state)  # list of coverage
            for i, block in enumerate(bc.block_list):
                efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency

def get_parameter_efficiency_one(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 2*n_qubit
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        n_parameter.append(block.n_parameter)
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for qubit in range(n_qubit):
        for state in range(2):
            coverage = get_coverage_one(bc, state_init, qubit, state)  # list of coverage
            for i, block in enumerate(bc.block_list):
                efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency


def get_coverage_two(bc: BlockCircuit, state_init='0000', qubit_i=1, qubit_j=0, state=0):
    n_qubit = len(state_init)
    if qubit_i > n_qubit*n_qubit - n_qubit - 1:
        raise ValueError('qubit shoud be valid index of qubits')
    if qubit_j >= qubit_i:
        raise ValueError('qubit_j should be less than qubit_i')
    if state > 3:
        raise ValueError('state shoud be in 0-3')

    init_set = []
    for i, value in enumerate(state_init):
        if value == '1':
            init_set.append(i)

    coverage = []
    init_block = HartreeFockInitBlock(init_set)
    optimizer = BasinhoppingOptimizer(random_initial=0.1)
    obj = TwoDMObjective(n_qubit, qubit_i, qubit_j, state)
    for i, block in enumerate(bc.block_list):
        circuit = BlockCircuit(n_qubit)
        circuit.add_block(init_block)
        for j in range(i + 1):
            circuit.add_block(bc.block_list[j])
        
        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        coverage.append(- np.real(coverage_high) - np.real(coverage_low))

    return coverage

def get_full_coverage_two(bc: BlockCircuit, n_qubit):
    normalize = 2*n_qubit*(n_qubit-1)
    efficiency = [0.0 for i in range(len(bc.block_list))]

    for position, block in enumerate(bc.block_list):
        coverage_high = [0.0 for i in range(normalize)]
        coverage_low = [1.0 for i in range(normalize)]
        for j in range(pow(2, n_qubit)):
            state_init = dec2bin(j, n_qubit)
            init_set = [] 
            for k, value in enumerate(state_init):
                if value == 1:
                    init_set.append(k)    
            
            init_block = HartreeFockInitBlock(init_set)
            circuit = BlockCircuit(n_qubit)
            circuit.add_block(init_block)
            for l in range(position + 1):
                circuit.add_block(bc.block_list[l])
            pcircuit = circuit.get_fixed_parameter_ansatz()

            TwoDM = evaluate_ansatz_2DMs([], pcircuit.n_qubit, pcircuit.ansatz)
            count = 0
            for qubit in range(n_qubit):
                for i in range(qubit):
                    for state in range(4):
                        coverage = np.real(TwoDM[qubit][i][state][state])
                        if coverage > coverage_high[count]:
                            coverage_high[count] = coverage
                        if coverage < coverage_low[count]:
                            coverage_low[count] = coverage
                        count += 1
        efficiency[position] = (sum(coverage_high) - sum(coverage_low)) / normalize

    return efficiency

def get_gate_efficiency_two(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 4*n_qubit*(n_qubit-1)
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        gates = block.get_gate_used()
        print(gates)
        n_parameter.append(2*gates['CNOT']+gates["SingleRotation"])
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for qubit in range(n_qubit):
        for j in range(qubit):
            for state in range(4):
                coverage = get_coverage_two(bc, state_init, qubit, j, state)  # list of coverage
                for i, block in enumerate(bc.block_list):
                    efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency

def get_parameter_efficiency_two(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 4*n_qubit*(n_qubit-1)
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        n_parameter.append(block.n_parameter)
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for qubit in range(n_qubit):
        for j in range(qubit):
            for state in range(4):
                coverage = get_coverage_two(bc, state_init, qubit, j, state)  # list of coverage
                for i, block in enumerate(bc.block_list):
                    efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency
 


def get_coverage(bc: BlockCircuit, state_init='0000', state_j='1111'):
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
        for j in range(i + 1):
            circuit.add_block(bc.block_list[j])
        circuit.add_block(final_block)
        optimizer = BasinhoppingOptimizer(
            random_initial=0.1)  # The initial parameter will be a random value between -0.1 and +0.1

        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        coverage.append(- np.real(coverage_high) - np.real(coverage_low))

    return coverage

def get_gate_efficiency(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 2**n_qubit
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        gates = block.get_gate_used()
        print(gates)
        n_parameter.append(2*gates['CNOT']+gates["SingleRotation"])
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for j in range(pow(2, n_qubit)):
        state = dec2bin(j, n_qubit)
        state_j = ''
        for value in state:
            state_j += str(value)

        coverage = get_coverage(bc, state_init, state_j)  # list of coverage
        for i, block in enumerate(bc.block_list):
            efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency

def get_parameter_efficiency(bc: BlockCircuit, state_init='0000'):
    n_qubit = len(state_init)
    normalize = 2**n_qubit
    efficiency = [0.0 for i in range(len(bc.block_list))]
    n_parameter = []

    for i, block in enumerate(bc.block_list):
        n_parameter.append(block.n_parameter)
        for j in range(i):
            n_parameter[i] += n_parameter[j]

    for j in range(pow(2, n_qubit)):
        state = dec2bin(j, n_qubit)
        state_j = ''
        for value in state:
            state_j += str(value)

        coverage = get_coverage(bc, state_init, state_j)  # list of coverage
        for i, block in enumerate(bc.block_list):
            efficiency[i] += coverage[i] / (n_parameter[i]*normalize)

    return efficiency


def output_region(bc: BlockCircuit, obj, state_init='0000'):
    n_qubit = len(state_init)
    efficiency = [0.0 for i in range(len(bc.block_list))]

    for i, block in enumerate(bc.block_list):
        circuit = BlockCircuit(n_qubit)
        circuit.add_block(init_block)
        for j in range(i + 1):
            circuit.add_block(bc.block_list[j])

        optimizer = BasinhoppingOptimizer(
            random_initial=0.1)  # The initial parameter will be a random value between -0.1 and +0.1

        coverage_low, para = optimizer.run_optimization(circuit, obj.get_cost())
        coverage_high, para = optimizer.run_optimization(circuit, obj.get_cost(maximum=True))
        region.append(- coverage_high - coverage_low)

    return region


