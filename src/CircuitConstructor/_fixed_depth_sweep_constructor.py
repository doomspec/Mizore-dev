from ._greedy_constructor import GreedyConstructor
from Objective._objective import Objective
from PoolGenerator import BlockPool

NOT_DEFINED = 999999

class FixedDepthSweepConstructor(GreedyConstructor):
    """
    Fixed depth sweep constructor which contains limited number of blocks.
    In the construction, the constructor first grow the circuit like GreedyConstrutor.
    After achieving the limit of block number, the constructor starts to sweep the blocks in the circuit
    and optimize the blocks in each position. In each position, both the type of block and its parameters will be optimized.

    Attributes:
        n_max_block: The maximal number of blocks that can be hold in the circuit.
        When the number is reached, the update of blocks will start from sweep_start_position.
        sweep_start_position: The position of block where the sweep starts.
        The default is 1 as the zero-th block is usually the HF initial block that should not by updated.

        Please see GreedyConstrutor for other attributes

    """
    CONSTRUCTOR_NAME="FixedDepthSweepConstructor"
    
    def __init__(self,*arg,n_max_block=5,sweep_start_position=1,**kwargs):
        GreedyConstructor.__init__(self,*arg,**kwargs)
        self.sweep_start_position=sweep_start_position
        self.position2update=sweep_start_position
        self.n_max_block=n_max_block
        self.n_non_decrease_steps=0

    def update_trial_circuits(self, block_pool=None):
        if block_pool == None:
            block_pool = self.block_pool
        if len(self.circuit.block_list)<self.n_max_block:
            GreedyConstructor.update_trial_circuits(self,block_pool=block_pool)
            return
        self.trial_circuits = []
        for block in block_pool:
            trial_circuit = self.circuit.duplicate()
            trial_circuit.block_list[self.position2update]=block
            trial_circuit.active_position_list=[self.position2update]
            #print(trial_circuit)
            self.trial_circuits.append(trial_circuit)
        self.position2update+=1
        if self.position2update==self.n_max_block:
            self.position2update=self.sweep_start_position

    def update_one_block(self):
        if len(self.circuit.block_list)>=self.n_max_block:
            print("Updating "+str(self.position2update)+"th block as the maximal block number has been met.")
        is_success=GreedyConstructor.update_one_block(self)
        if len(self.circuit.block_list)>=self.n_max_block:
            if is_success:
                self.n_non_decrease_steps=0
                return True
            else:
                self.n_non_decrease_steps+=1
                if self.n_non_decrease_steps>=self.n_max_block-self.sweep_start_position:
                    return False
                else:
                    return True
        else:
            return is_success


