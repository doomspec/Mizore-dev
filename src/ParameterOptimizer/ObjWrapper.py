from Blocks._parametrized_circuit import ParametrizedCircuit
from Utilities.CircuitEvaluation import evaluate_circuit_energy


def get_obj_for_optimizer(pcircuit: ParametrizedCircuit, hamiltonian):
    def obj(parameter):
        return evaluate_circuit_energy(parameter, pcircuit.n_qubit, hamiltonian, pcircuit.ansatz)

    return obj