from CircuitConstructor._circuit_constructor import *
from ParameterOptimizer._circuit_optimizer import basinhopping_optimizer
from Blocks._block import Block
from multiprocessing import Process
from copy import copy, deepcopy
from Blocks._utilities import *
from Objective._hamiltonian_obj import HamiltonianObjective


class GreedyConstructor(CircuitConstructor):

    def __init__(self, hamiltonian_obj: HamiltonianObjective, block_pool, max_n_block=100, terminate_energy=-NOT_DEFINED):

        Process.__init__(self)

        self.circuit = BlockCircuit(hamiltonian_obj.n_qubit)
        self.max_n_block = max_n_block
        self.terminate_energy = terminate_energy
        self.block_pool = block_pool
        self.n_qubit = hamiltonian_obj.n_qubit
        self.hamiltonian = hamiltonian_obj.hamiltonian
        self.circuit.add_block(hamiltonian_obj.init_block)
        if "terminate_energy" in hamiltonian_obj.obj_info.keys():
            self.terminate_energy = hamiltonian_obj.obj_info["terminate_energy"]

        return

    def run(self):
        print("Here is GreedyConstructor")
        print("Size of Block Pool:", len(self.block_pool.blocks))
        self.init_energy = self.circuit.get_energy(self.hamiltonian)
        self.current_energy = self.init_energy
        print("Initial Energy:", self.init_energy)
        for layer in range(self.max_n_block):
            if self.add_one_block():
                # Succeed to add new block
                print(self.circuit)
                if self.when_terminate_energy_achieved!=-1:
                    print("Target energy achieved by", self.when_terminate_energy_achieved," blocks!")
                    print("Construction process ends!")
                    return
            else:
                # Fail to add new block
                return
        return

    def add_one_block(self):
        """Try to add a new block
        Return True is succeed, return False otherwise
        """
        trial_result_list = self.do_trial_on_blocks()
        best_block = self.get_block_by_trial_result(trial_result_list)
        if best_block!=None:
            self.circuit.add_block(best_block)
            print("Block added, energy now is:", self.current_energy, "Hartree")
            print("Distance to target energy:",self.current_energy-self.terminate_energy)
            if self.current_energy<=self.terminate_energy:
                self.when_terminate_energy_achieved=len(self.circuit.block_list)
            return True
        else:
            print("No entangler in the pool provides a lower energy")
            print("A larger pool is needed or Ground energy was achieved")
            return False

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

        # See whether the new entangler decreases the energy,
        # otherwise return None
        if best_result[1]>0: 
            new_block = copy(best_result[3])
            new_block.parameter = best_result[2]
            self.current_energy = best_result[0]
            return new_block
        else:
            return None
