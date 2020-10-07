import numpy as np

from ._objective import Objective, CostFunction
from Blocks import HartreeFockInitBlock

class AmplitudeObjective(Objective):
    """
    Attributes:
        final_block: the final state to be measure
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
        return AmplitudeCost(maximum)


from Utilities.CircuitEvaluation import evaluate_ansatz_0000_amplitudes

class AmplitudeCost(CostFunction):
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


class OneDMObjective(Objective):
    """
    Attributes:
        n_qubit: number of qubits.
        qubit: qubit index.
        state: state in 1rdm.
        obj_info: The dict for additional information of the Hamiltonian, e.g. the HF energy and the ground state energy
    Methods:
        get_cost(): generate a Cost object which can be used by optimizers
    """

    def __init__(self, n_qubit, qubit=0, state=0, obj_info={}):
        self.n_qubit = n_qubit
        self.obj_info = obj_info
        self.qubit = qubit
        self.state = state
        return

    def get_cost(self, maximum = False):
        return OneDMCost(maximum, self.qubit, self.state)


from Utilities.CircuitEvaluation import evaluate_ansatz_1DMs

class OneDMCost(CostFunction):
    def __init__(self, maximum=False, qubit=0, state=0):
        self.maximum = maximum
        self.qubit = qubit
        self.state = state

    def get_cost_obj(self, circuit):
        pcircuit = circuit.get_ansatz_on_active_position()
        qubit = self.qubit
        state = self.state
        
        def obj(parameter):
            OneDM = evaluate_ansatz_1DMs(parameter, pcircuit.n_qubit, pcircuit.ansatz)
            #print(OneDM)
            probability = OneDM[qubit][state][state]
            if self.maximum :
                coverage = -probability
            else: 
                coverage = probability

            return coverage

        return obj

    def get_cost_value(self, circuit):
        pcircuit = circuit.get_fixed_parameter_ansatz()
        qubit = self.qubit
        state = self.state
        OneDM = evaluate_ansatz_1DMs([], pcircuit.n_qubit, pcircuit.ansatz)
        amp = OneDM[qubit][state][state]
        if self.maximum :
            coverage = -amp
        else: 
            coverage = amp
        return coverage


class TwoDMObjective(Objective):
    """
    Attributes:
        n_qubit: number of qubits.
        qubit: qubit pair index.
        state: state in 1rdm.
        obj_info: The dict for additional information of the Hamiltonian, e.g. the HF energy and the ground state energy
    Methods:
        get_cost(): generate a Cost object which can be used by optimizers
    """

    def __init__(self, n_qubit, qubit_i=1, qubit_j=0, state=0, obj_info={}):
        self.n_qubit = n_qubit
        self.obj_info = obj_info
        self.qubit_i = qubit_i
        self.qubit_j = qubit_j
        self.state = state
        return

    def get_cost(self, maximum = False):
        return TwoDMCost(maximum, self.qubit_i, self.qubit_j, self.state)


from Utilities.CircuitEvaluation import evaluate_ansatz_2DMs

class TwoDMCost(CostFunction):
    def __init__(self, maximum=False, qubit_i=1, qubit_j=0, state=0):
        self.maximum = maximum
        self.qubit_i = qubit_i
        self.qubit_j = qubit_j
        self.state = state

    def get_cost_obj(self, circuit):
        pcircuit = circuit.get_ansatz_on_active_position()
        
        def obj(parameter):
            TwoDM = evaluate_ansatz_2DMs(parameter, pcircuit.n_qubit, pcircuit.ansatz)
            probability = TwoDM[self.qubit_i][self.qubit_j][self.state][self.state]
            if self.maximum :
                coverage = -probability
            else: 
                coverage = probability

            return coverage

        return obj

    def get_cost_value(self, circuit):
        pcircuit = circuit.get_fixed_parameter_ansatz()
        TwoDM = evaluate_ansatz_2DMs([], pcircuit.n_qubit, pcircuit.ansatz)
        probability = TwoDM[self.qubit_i][self.qubit_j][self.state][self.state]
        if self.maximum :
            coverage = -probability
        else: 
            coverage = probability
        return coverage