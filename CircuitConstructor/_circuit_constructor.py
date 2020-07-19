from Entanglers._entangler_circuit import EntanglerCircuit
from multiprocessing import Process
NOT_DEFINED = 999999

class CircuitConstructor(Process):

    entangler_pool=None
    circuit:EntanglerCircuit=None
    init_energy = NOT_DEFINED
    terminate_energy = -NOT_DEFINED
    when_terminate_energy_achieved = -1
    current_energy = NOT_DEFINED

    def __init__(self):
        return
