from ._objective import Objective, CostFunction
from ..Blocks import HartreeFockInitBlock
from ..Blocks._utilities import get_circuit_energy
from ..Utilities.CircuitEvaluation import evaluate_ansatz_1DMs
from ..Blocks._utilities import concatenate_circuit
from ..Utilities.WaveLocalProperties import purity_one_DM


class PurityObjective(Objective):
    """

    """

    def __init__(self, circuits, qsubset, circuit_weights=None, obj_info={}):
        self.circuits = circuits
        self.n_qubit = circuits[0].n_qubit
        Objective.__init__(self, n_qubit=self.n_qubit)
        self.qsubset = qsubset
        self.obj_info = obj_info
        self.obj_info["terminate_cost"] = -len(qsubset)
        self.n_circuit = len(circuits)
        self.circuit_weights = None
        self.set_circuit_weights(circuit_weights)

    def set_circuit_weights(self, circuit_weights):
        if circuit_weights == None:
            self.circuit_weights = [1 / self.n_circuit] * self.n_circuit
        else:
            assert self.n_circuit == len(circuit_weights)
            self.circuit_weights = circuit_weights
            weight_sum = sum(circuit_weights)
            if abs(weight_sum - 1) > 1e-7:
                for i in range(len(circuit_weights)):
                    self.circuit_weights[i] /= weight_sum

    def get_cost(self):
        return PurityCost(self.circuits, self.qsubset, self.circuit_weights)


class PurityCost(CostFunction):
    def __init__(self, circuits, qsubset, circuit_weights):
        self.circuits = circuits
        self.qsubset = qsubset
        self.circuit_weights = circuit_weights

    def get_cost_obj(self, circuit):
        def obj(parameter):
            purity_sum = 0
            for i in range(len(self.circuits)):
                temp_circuit = self.circuits[i].duplicate()
                temp_circuit.active_position_list = []
                temp_circuit = concatenate_circuit(temp_circuit, circuit)
                pcircuit = temp_circuit.get_ansatz_on_active_position()

                one_DMs = evaluate_ansatz_1DMs(parameter, pcircuit.n_qubit, pcircuit.ansatz)
                purities = [purity_one_DM(one_DMs[i]) for i in range(len(one_DMs))]
                circuit_purity_sum = 0
                for j in self.qsubset:
                    circuit_purity_sum += purities[j]
                circuit_purity_sum *= self.circuit_weights[i]
                purity_sum += circuit_purity_sum
            return -purity_sum

        return obj

    def get_cost_value(self, circuit):
        purity_sum = 0
        for i in range(len(self.circuits)):
            temp_circuit = concatenate_circuit(self.circuits[i].duplicate(), circuit)
            pcircuit = temp_circuit.get_fixed_parameter_ansatz()
            one_DMs = evaluate_ansatz_1DMs([0] * 100, pcircuit.n_qubit, pcircuit.ansatz)
            purities = [purity_one_DM(one_DMs[i]) for i in range(len(one_DMs))]
            circuit_purity_sum = 0
            for j in self.qsubset:
                circuit_purity_sum += purities[j]
            circuit_purity_sum *= self.circuit_weights[i]
            purity_sum += circuit_purity_sum
        return -purity_sum
