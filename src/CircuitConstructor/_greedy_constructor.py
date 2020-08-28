from CircuitConstructor._circuit_constructor import CircuitConstructor
from Blocks import Block, BlockCircuit
from PoolGenerator import BlockPool
from multiprocessing import Process
from copy import copy, deepcopy
from Blocks._utilities import *
from Objective._objective import Objective
from ParallelTaskRunner import TaskManager, OptimizationTask, GradientTask
from ParameterOptimizer import BasinhoppingOptimizer, ImaginaryTimeEvolutionOptimizer
from ._result_display import save_construction
import time
import numpy
import math
NOT_DEFINED = 999999


class GreedyConstructor(CircuitConstructor):
    """
    Greedy circuit constructor which try all the blocks in self.block_pool in each iteration 
    and add the block that decrease the cost most in the *end* of the self.circuit.

    This strategy is used in the following works
    J. Chem. Theory Comput. 2020, 16, 2
    Nat Commun 10, 3007 (2019)

    Attributes:
        construct_obj: a Objective that defines the problem (like EnergyObjective for ground state energy)
        block_pool: The BlockPool used for contruct the circuit, will be gone over at each iteration
        circuit: the circuit kept by the constructor, should be contructed when running
        max_n_iter: Max number of blocks to be added in the circuit
        terminate_cost: the cost where the construction stops
        optimizer: a ParameterOptimizer for parameter optimization
        task_manager: a TaskManager for parallel run of parameter optimization. 
        If left None, a new task manager uses 4 processes will be created and used 
    """

    gradiant_cutoff = 1e-9

    def __init__(self, construct_obj: Objective, block_pool: BlockPool, max_n_iter=100, gradient_screening_rate=0.1, terminate_cost=-NOT_DEFINED, optimizer=BasinhoppingOptimizer(), task_manager: TaskManager = None, init_circuit=None, project_name=None):

        CircuitConstructor.__init__(self)
        self.circuit = init_circuit
        if self.circuit == None:
            self.circuit = BlockCircuit(construct_obj.n_qubit)
            self.circuit.add_block(construct_obj.init_block)
        self.max_n_iter = max_n_iter
        self.terminate_cost = terminate_cost
        self.gradient_screening_rate = gradient_screening_rate
        self.block_pool = block_pool
        self.n_qubit = construct_obj.n_qubit
        self.cost = construct_obj.get_cost()
        self.id = id(self)
        self.optimizer = optimizer
        self.time_string = time.strftime(
            '%m-%d-%Hh%Mm%Ss', time.localtime(time.time()))
        self.project_name = project_name+"_"+self.time_string
        self.trial_circuits = []
        if "terminate_cost" in construct_obj.obj_info.keys():
            self.terminate_cost = construct_obj.obj_info["terminate_cost"]

        self.task_manager = task_manager
        self.task_manager_created = False
        if task_manager == None:
            self.task_manager = TaskManager(n_processor=4)
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
        self.start_time_number = time.time()
        self.add_time_point()
        for i_iter in range(self.max_n_iter):
            print("********The "+str(i_iter+1)+"th Iteration*********")
            self.update_trial_circuits()
            is_succeed = self.update_one_block()
            is_return = False
            if is_succeed:
                # Succeed to add new block
                if self.when_terminate_cost_achieved != -1:
                    if self.task_manager_created:
                        self.task_manager.close()
                    is_return = True
            else:
                # Fail to add new block
                print("Circuit update failed")
                print("Suggestion: 1.Use larger pool 2.Ground cost may have achieved")
                print("Final Energy:", self.current_cost)
                print("********Final Circuit********")
                print(self.circuit)
                if self.task_manager_created:
                    self.task_manager.close()
                is_return = True
            self.add_time_point()
            save_construction(self, self.project_name)
            if is_return:
                return
        return

    def do_global_optimization(self):

        self.circuit.set_all_block_active()
        task = OptimizationTask(self.circuit, BasinhoppingOptimizer(
            random_initial=0.0), self.cost)
        self.current_cost, parameter = task.run()
        self.circuit.adjust_parameter_on_active_position(parameter)
        self.cost_list.append(self.current_cost)
        save_construction(self, self.project_name)


    def update_one_block(self):
        """Try to add a new block
        Return True is succeed, return False otherwise
        """
        trial_result_list = self.do_trial_on_circuits_by_cost_gradient()
        if len(trial_result_list) != 0:
            self.update_circuit_by_trial_result(trial_result_list)
            print("Block added and shown below, cost now is:",
                  self.current_cost, "Hartree")
            print("********New Circuit********")
            print(self.circuit)
            print("Doing global optimization on the new circuit")
            self.do_global_optimization()
            print("Global Optimized Energy:", self.current_cost)
            print("Distance to target cost:",
                  self.current_cost - self.terminate_cost)
            print("Gate Usage:", self.circuit.get_gate_used())
            print("Energy list:", self.cost_list)
            if self.current_cost <= self.terminate_cost:
                self.when_terminate_cost_achieved = len(
                    self.circuit.block_list)
                print("Target cost achieved by",
                          self.when_terminate_cost_achieved, " blocks!")
                print("Construction process ends!")
            return True
        else:
            print("No trial circuit in the list provides a lower cost")
            return False

    def update_trial_circuits(self, block_pool=None):
        if block_pool == None:
            block_pool = self.block_pool
        self.trial_circuits = []
        for block in block_pool:
            trial_circuit = self.circuit.duplicate()
            trial_circuit.add_block(block)
            trial_circuit.set_only_last_block_active()
            self.trial_circuits.append(trial_circuit)

    def do_trial_on_circuits_by_cost_value(self, trial_circuits=None):
        if trial_circuits == None:
            trial_circuits = self.trial_circuits
        task_series_id="Single Block Optimize "+str(self.id%100000)
        trial_result_list = []
        for trial_circuit in trial_circuits:
            task = OptimizationTask(trial_circuit, self.optimizer, None)
            self.task_manager.add_task_to_buffer(task, task_series_id=task_series_id)
        self.task_manager.flush(public_resource={"cost": self.cost})
        res_list = self.task_manager.receive_task_result(
            task_series_id=task_series_id,progress_bar=True)
        for i in range(len(trial_circuits)):
            cost, amp = res_list[i]
            cost_descent = self.current_cost - cost
            # See whether the new entangler decreases the cost
            if cost_descent > GreedyConstructor.gradiant_cutoff:
                trial_circuits[i].adjust_parameter_on_active_position(amp)
                trial_result_list.append((cost, trial_circuits[i]))
        return trial_result_list

    def do_trial_on_circuits_by_cost_gradient(self, trial_circuits=None):
        if trial_circuits == None:
            trial_circuits = self.trial_circuits
        if abs(self.gradient_screening_rate-1) < 0.00001:
            return self.do_trial_on_circuits_by_cost_value()

        task_series_id="Gradient "+str(self.id%100000)

        for trial_circuit in trial_circuits:
            task = GradientTask(trial_circuit, None)
            self.task_manager.add_task_to_buffer(task, task_series_id=task_series_id)
        self.task_manager.flush(public_resource={"cost": self.cost})
        res_list = self.task_manager.receive_task_result(task_series_id=task_series_id,progress_bar=True)
        res_list = [numpy.linalg.norm(res) for res in res_list]
        res_list = numpy.array(res_list)
        n_circuit_to_try = math.ceil(
            self.gradient_screening_rate*len(trial_circuits))
        rank_list = (-1*res_list).argsort()[:n_circuit_to_try]
        good_circuits = []
        for i in rank_list:
            good_circuits.append(trial_circuits[i])
        return self.do_trial_on_circuits_by_cost_value(trial_circuits=good_circuits)

    def update_circuit_by_trial_result(self, trial_result_list):
        lowest_cost = NOT_DEFINED
        lowest_cost_index = -1
        for i in range(len(trial_result_list)):
            if trial_result_list[i][0] < lowest_cost:
                lowest_cost = trial_result_list[i][0]
                lowest_cost_index = i
        best_result = trial_result_list[lowest_cost_index]
        self.current_cost = best_result[0]
        self.circuit = best_result[1]
