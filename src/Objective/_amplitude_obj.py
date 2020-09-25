import numpy as np

from ._objective import Objective, CostFunction
from Blocks import HartreeFockInitBlock

class AmplitudeObjective(Objective):
    """
    Attributes:
        init_block: the block usually used for initiate the wave fucntion for the Hamiltonian.
        A block that produce a state near the ground state should be adopted.
        Usually, for the molecule, the Hartree Fock initialization is used
        obj_info: The dict for additional information of the Hamiltonian, e.g. the HF energy and the ground state energy
    Methods:
        get_cost(): generate a Cost object which can be used by optimizers
    """

    def __init__(self, n_qubit, final_block=None, obj_info={}):
        self.n_qubit = n_qubit
        self.obj_info = obj_info
        if final_block != None:
            self.final_block = final_block
        return

    def get_cost(self, maximum = False):
        return Cost(maximum)


from Utilities.CircuitEvaluation import evaluate_ansatz_0000_amplitudes

class Cost(CostFunction):
    def __init__(self, maximum=False):
        self.maximum = maximum

    def get_cost_obj(self, circuit):
        pcircuit = circuit.get_ansatz_on_active_position()
        
        def obj(parameter):
            amp = evaluate_ansatz_0000_amplitudes(pcircuit.n_qubit, pcircuit.ansatz, parameter)
            if self.maximum :
                coverage = -amp*np.conjugate(amp)
            else: 
                coverage = amp*np.conjugate(amp)

            return coverage

        return obj

    def get_cost_value(self, circuit):
        pcircuit = circuit.get_fixed_parameter_ansatz()
        amp = evaluate_ansatz_0000_amplitudes(pcircuit.n_qubit, pcircuit.ansatz)
        if self.maximum :
            coverage = -amp*np.conjugate(amp)
        else: 
            coverage = amp*np.conjugate(amp)
        return coverage
