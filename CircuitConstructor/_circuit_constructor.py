from Blocks._block_circuit import BlockCircuit
from multiprocessing import Process
NOT_DEFINED = 999999

class CircuitConstructor(Process):

    def __init__(self):

        self.block_pool=None
        self.circuit:BlockCircuit=None
        self.init_energy = NOT_DEFINED
        self.terminate_energy = -NOT_DEFINED
        self.when_terminate_energy_achieved = -1
        self.current_energy = NOT_DEFINED
        self.init_operator=None
        
        return
