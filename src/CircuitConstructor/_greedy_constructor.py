from CircuitConstructor._circuit_constructor import CircuitConstructor
from Blocks import Block, BlockCircuit
from PoolGenerator import BlockPool
from multiprocessing import Process
from copy import copy, deepcopy
from Blocks._utilities import *
from Objective._objective import Objective
from ParallelTaskRunner import TaskManager, OptimizationTask
from ParameterOptimizer import BasinhoppingOptimizer, ImaginaryTimeEvolutionOptimizer
from ._result_display import save_circuit
import time
NOT_DEFINED = 999999


class GreedyConstructor(CircuitConstructor):
    """
    Greedy circuit constructor which try all the blocks in self.block_pool in each iteration 
    and add the block that decrease the cost most to the self.circuit.

    This strategy is used in the following works
    J. Chem. Theory Comput. 2020, 16, 2
    Nat Commun 10, 3007 (2019)

    Attributes:
        hamiltonian: a Hamiltonian that defines the problem
        circuit: the circuit kept by the constructor, should be developed when running
        max_n_block: Max number of blocks to be added in the circuit
        terminate_cost: the cost where the construction stops
        optimizer: a ParameterOptimizer for parameter optimization
        task_manager: a TaskManager for parallel run of parameter optimization. 
        If left None, a new task manager uses 4 processes will be created and used 

    """

    gradiant_cutoff = 1e-9

    def __init__(self, construct_obj: Objective, block_pool: BlockPool, max_n_block=100, terminate_cost=-NOT_DEFINED, optimizer=BasinhoppingOptimizer(), task_manager: TaskManager = None, init_circuit=None, project_name=None):

        CircuitConstructor.__init__(self)
        self.circuit = init_circuit
        if self.circuit == None:
            self.circuit = BlockCircuit(construct_obj.n_qubit)
            self.circuit.add_block(construct_obj.init_block)
        self.max_n_block = max_n_block
        self.terminate_cost = terminate_cost
        self.block_pool = block_pool
        self.n_qubit = construct_obj.n_qubit
        self.cost = construct_obj.get_cost()
        self.id = id(self)
        self.optimizer = optimizer
        self.project_name = project_name
        self.time_string=time.strftime('%m-%d-%Hh%Mm%Ss', time.localtime(time.time()))
        self.cost_list = []

        if "terminate_cost" in construct_obj.obj_info.keys():
            self.terminate_cost = construct_obj.obj_info["terminate_cost"]

        self.task_manager = task_manager
        self.task_manager_created = False
        if task_manager == None:
            self.task_manager = TaskManager()
            self.task_manager_created = True
        return

    def run(self):
        print("Here is GreedyConstructor")
        print("Project Name:", self.project_name)
        print("Block Pool Size:", len(self.block_pool.blocks))
        self.init_cost = self.cost.get_cost_value(self.circuit)
        self.current_cost = self.init_cost
        self.cost_list.append(self.current_cost)
        print("Initial Energy:", self.init_cost)
        # print(self.block_pool)
        for _layer in range(self.max_n_block):
            print("********Adding "+str(_layer+1)+"th Block*********")
            if self.add_one_block():
                # Succeed to add new block
                print(self.circuit)
                self.do_global_optimization()
                if self.when_terminate_cost_achieved != -1:
                    print("Target cost achieved by",
                          self.when_terminate_cost_achieved, " blocks!")
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
        task = OptimizationTask(self.circuit, BasinhoppingOptimizer(
            random_initial=0.0), self.cost)
        self.current_cost, parameter = task.run()
        self.circuit.adjust_parameter_on_active_position(parameter)
        self.cost_list.append(self.current_cost)
        save_circuit(self.circuit,self.project_name+"_"+self.time_string)
        print("Global Optimized Energy:", self.current_cost)
        print("Gate Usage:", self.circuit.get_gate_used())
        print("Energy list:", self.cost_list)

    def add_one_block(self):
        """Try to add a new block
        Return True is succeed, return False otherwise
        """
        trial_result_list = self.do_trial_on_blocks()
        best_block = self.get_block_by_trial_result(trial_result_list)
        if best_block != None:
            self.circuit.add_block(best_block)
            print("Block added, cost now is:",
                  self.current_cost, "Hartree")
            print("Distance to target cost:",
                  self.current_cost - self.terminate_cost)
            if self.current_cost <= self.terminate_cost:
                self.when_terminate_cost_achieved = len(
                    self.circuit.block_list)
            return True
        else:
            print("No entangler in the pool provides a lower cost")
            print("A larger pool is needed or Ground cost was achieved")
            print("Final Energy:", self.current_cost)
            print("********Final Circuit********")
            print(self.circuit)
            return False

    def do_trial_on_blocks(self):
        trial_result_list = []
        for block in self.block_pool:
            # print(block)
            trial_circuit = self.circuit.duplicate()
            trial_circuit.add_block(block)
            trial_circuit.set_only_last_block_active()
            task = OptimizationTask(
                trial_circuit, self.optimizer, self.cost)
            self.task_manager.add_task_to_buffer(task, task_series_id=self.id)
        self.task_manager.flush(task_series_id=self.id)
        res_list = self.task_manager.receive_task_result(
            task_series_id=self.id)
        i = 0
        for block in self.block_pool:
            cost, amp = res_list[i]
            cost_descent = self.current_cost - cost
            trial_result_list.append((cost, cost_descent, amp, block))
            i += 1
        return trial_result_list

    def get_block_by_trial_result(self, trial_result_list):

        lowest_cost = NOT_DEFINED
        lowest_cost_index = -1
        for i in range(len(trial_result_list)):
            if trial_result_list[i][0] < lowest_cost:
                lowest_cost = trial_result_list[i][0]
                lowest_cost_index = i
        best_result = trial_result_list[lowest_cost_index]

        # See whether the new entangler decreases the cost,
        # otherwise return None
        if best_result[1] > GreedyConstructor.gradiant_cutoff:
            new_block = copy(best_result[3])
            new_block.adjust_parameter(best_result[2])
            self.current_cost = best_result[0]
            return new_block
        else:
            return None
