from multiprocessing import Process

NOT_DEFINED = 999999


class CircuitConstructor(Process):

    def __init__(self):
        Process.__init__(self)

        self.block_pool = None
        self.circuit = None  # Should be a BlockCircuit
        self.init_energy = NOT_DEFINED
        self.terminate_energy = -NOT_DEFINED
        self.when_terminate_energy_achieved = -1
        self.current_energy = NOT_DEFINED
        self.init_operator = None

        return
