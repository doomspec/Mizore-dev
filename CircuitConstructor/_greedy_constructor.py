from CircuitConstructor._circuit_constructor import CircuitConstructor
from Blocks import Block, BlockCircuit
from PoolGenerator import BlockPool
from multiprocessing import Process
from copy import copy, deepcopy
from Blocks._utilities import *
from Objective._hamiltonian_obj import HamiltonianObjective
from ParallelTaskRunner import TaskManager, OptimizationTask
from ParameterOptimizer import BasinhoppingOptimizer, ImaginaryTimeEvolutionOptimizer
from Blocks._utilities import get_inner_two_circuit_product, get_circuit_energy

NOT_DEFINED = 999999


class GreedyConstructor(CircuitConstructor):
    """
    Greedy circuit constructor which try all the blocks in self.block_pool in each iteration 
    and add the block that decrease the energy most to the self.circuit.

    This strategy is used in the following works
    J. Chem. Theory Comput. 2020, 16, 2
    Nat Commun 10, 3007 (2019)

    Attributes:
        hamiltonian: a Hamiltonian that defines the problem
        circuit: the circuit kept by the constructor, should be developed when running
        max_n_block: Max number of blocks to be added in the circuit
        terminate_energy: the energy where the construction stops
        optimizer: a ParameterOptimizer for parameter optimization
        task_manager: a TaskManager for parallel run of parameter optimization. 
        If left None, a new task manager uses 4 processes will be created and used 

    """

    gradiant_cutoff = 1e-9

    def __init__(self, hamiltonian_obj: HamiltonianObjective, block_pool: BlockPool, max_n_block=100, terminate_energy=-NOT_DEFINED, optimizer=BasinhoppingOptimizer() ,task_manager: TaskManager = None):
        """
        
        """
        CircuitConstructor.__init__(self)

        self.circuit = BlockCircuit(hamiltonian_obj.n_qubit)
        self.max_n_block = max_n_block
        self.terminate_energy = terminate_energy
        self.block_pool = block_pool
        self.n_qubit = hamiltonian_obj.n_qubit
        self.hamiltonian = hamiltonian_obj.hamiltonian
        self.circuit.add_block(hamiltonian_obj.init_block)
        self.id = id(self)
        self.optimizer=optimizer
        
        self.energy_list=[]

        if "terminate_energy" in hamiltonian_obj.obj_info.keys():
            self.terminate_energy = hamiltonian_obj.obj_info["terminate_energy"]
        self.task_manager = task_manager
        self.task_manager_created=False
        if task_manager == None:
            # If task_manager not specified, use 4 processors manager
            self.task_manager = TaskManager(4)
            self.task_manager_created = True
        return

    def run(self):
        print("Here is GreedyConstructor")
        print("Size of Block Pool:", len(self.block_pool.blocks))
        self.init_energy = get_circuit_energy(self.circuit, self.hamiltonian)
        self.current_energy = self.init_energy
        self.energy_list.append(self.current_energy)
        print("Initial Energy:", self.init_energy)
        # print(self.block_pool)
        for layer in range(self.max_n_block):
            if self.add_one_block():
                # Succeed to add new block
                print(self.circuit)
                self.do_global_optimization()
                if self.when_terminate_energy_achieved != -1:
                    print("Target energy achieved by",
                          self.when_terminate_energy_achieved, " blocks!")
                    print("Construction process ends!")
                    if self.task_manager_created:
                        self.task_manager.close()
                    return
            else:
                # Fail to add new block
                if self.task_manager_created:
                    self.task_manager.close()
                return
        return

    def do_global_optimization(self):
        print("Doing global optimization")
        self.circuit.set_all_block_active()
        task=OptimizationTask(self.circuit,BasinhoppingOptimizer(random_initial=0.0),self.hamiltonian)
        self.current_energy,parameter=task.run()
        self.circuit.adjust_parameter_on_active_position(parameter)
        self.energy_list.append(self.current_energy)
        print("Global Optimized Energy:",self.current_energy)

    def add_one_block(self):
        """Try to add a new block
        Return True is succeed, return False otherwise
        """
        trial_result_list = self.do_trial_on_blocks()
        best_block = self.get_block_by_trial_result(trial_result_list)
        if best_block != None:
            self.circuit.add_block(best_block)
            print("Block added, energy now is:",
                  self.current_energy, "Hartree")
            print("Distance to target energy:",
                  self.current_energy - self.terminate_energy)
            if self.current_energy <= self.terminate_energy:
                self.when_terminate_energy_achieved = len(
                    self.circuit.block_list)
            return True
        else:
            print("No entangler in the pool provides a lower energy")
            print("A larger pool is needed or Ground energy was achieved")
            print("Final Energy:", self.current_energy)
            print("Final Circuit:")
            print(self.circuit)
            return False

    def do_trial_on_blocks(self):
        trial_result_list = []
        for block in self.block_pool:
            # print(block)
            trial_circuit = self.circuit.duplicate()
            trial_circuit.add_block(block)
            trial_circuit.set_only_last_block_active()
            task=OptimizationTask(trial_circuit,self.optimizer,self.hamiltonian)
            self.task_manager.add_task(task, task_series_id=self.id)

        res_list = self.task_manager.receive_task_result(
            task_series_id=self.id)
        i = 0
        for block in self.block_pool:
            energy, amp = res_list[i]
            energy_descent = self.current_energy - energy
            trial_result_list.append((energy, energy_descent, amp, block))
            i += 1
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
        if best_result[1] > GreedyConstructor.gradiant_cutoff:
            new_block = copy(best_result[3])
            new_block.adjust_parameter(best_result[2])
            self.current_energy = best_result[0]
            return new_block
        else:
            return None
