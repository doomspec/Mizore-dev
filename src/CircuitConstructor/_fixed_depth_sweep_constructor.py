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


class FixedDepthSweepConstructor(CircuitConstructor):
    """
    Fixed depth sweep constructor which contains limited number of blocks.
    In the construction, the constructor first grow the circuit like GreedyConstrutor.
    After achieving the limit of block number, the constructor starts to sweep the blocks in the circuit
    and optimize the blocks in each position. In each position, both the type of block and its parameter will be optimized.

    NOT FINISHED!!
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
        return