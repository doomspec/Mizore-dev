from CircuitConstructor._circuit_constructor import *
from ParameterOptimizer._circuit_optimizer import basinhopping_optimizer
from Blocks._block import Block
from multiprocessing import Process
from copy import copy, deepcopy
from Blocks._utilities import *



class GreedyConstructor(CircuitConstructor):

    def __init__(self, n_qubit, hamiltonian, block_pool, max_n_block=100, terminate_energy=-NOT_DEFINED):

        Process.__init__(self)

        self.circuit = BlockCircuit(n_qubit)
        self.max_n_block = max_n_block
        self.terminate_energy = terminate_energy
        self.block_pool = block_pool
        self.n_qubit = n_qubit
        self.hamiltonian = hamiltonian

        return

    def run(self):
        print("Here is GreedyConstructor")
        print("Size of Block Pool:", len(self.block_pool.blocks))
        #print(self.block_pool)
        self.init_energy = self.circuit.get_energy(self.hamiltonian)
        self.current_energy = self.init_energy
        print("Initial Energy:", self.init_energy)
        for layer in range(self.max_n_block):
            self.add_one_block()
            print(self.circuit)
            #print(concatenate_circuit(self.circuit,get_inverse_circuit(self.circuit)))
        return

    def add_one_block(self):
        trial_result_list = self.do_trial_on_blocks()
        best_block = self.get_block_by_trial_result(trial_result_list)
        self.circuit.add_block(best_block)
        print("Block added, energy now is:", self.current_energy)
        return

    def do_trial_on_blocks(self):
        trial_result_list = []
        for block in self.block_pool:
            trial_circuit = self.circuit.duplicate()
            trial_circuit.add_block(block)
            pcircuit = trial_circuit.get_ansatz_last_block()
            energy, amp = basinhopping_optimizer(
                pcircuit, self.hamiltonian)
            energy_descent = energy-self.current_energy
            trial_result_list.append((energy, energy_descent, amp, block))
        return trial_result_list

    def get_block_by_trial_result(self, trial_result_list):
        lowest_energy = NOT_DEFINED
        lowest_energy_index = -1
        for i in range(len(trial_result_list)):
            if trial_result_list[i][0] < lowest_energy:
                lowest_energy = trial_result_list[i][0]
                lowest_energy_index = i
        best_result = trial_result_list[lowest_energy_index]
        new_block = copy(best_result[3])
        new_block.parameter = best_result[2]
        self.current_energy = best_result[0]
        return new_block
