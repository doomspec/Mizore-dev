from multiprocessing import Process

NOT_DEFINED = 999999


class CircuitConstructor(Process):
    """
    The base class of all circuit construtor
    Attributes:
        block_pool
        circuit
        init_cost
        terminate_cost
    """
    def __init__(self):
        Process.__init__(self)

        self.block_pool = None
        self.circuit = None  # Should be a BlockCircuit
        self.init_cost = NOT_DEFINED
        self.terminate_cost = -NOT_DEFINED
        self.when_terminate_cost_achieved = -1
        self.current_cost = NOT_DEFINED
        self.init_operator = None

        return
    def execute_construction(self):
        self.start()
        self.join()
        self.terminate()
        return self.circuit