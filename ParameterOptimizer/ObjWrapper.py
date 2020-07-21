
from projectq import MainEngine
from projectq.ops import X, All, Measure, CNOT, Z, Rz, Rx, C, TimeEvolution
from projectq.backends import CommandPrinter, CircuitDrawer, Simulator
from projectq.meta import Loop, Compute, Uncompute, Control

from projectq.cengines import (MainEngine,
                               AutoReplacer,
                               LocalOptimizer,
                               TagRemover,
                               DecompositionRuleSet)
import projectq.setups.decompositions
from Blocks._parametrized_circuit import ParametrizedCircuit


def get_obj_for_optimizer(pcircuit: ParametrizedCircuit, hamiltonian):
    def obj(parameter):
        return evaluate_circuit_energy(parameter, pcircuit.n_qubit, hamiltonian, pcircuit.ansatz)
    return obj


def evaluate_circuit_energy(parameter, n_qubit, hamiltonian, ansatz):
    """
    Args:

    Returns:

    """
    # Create a main compiler engine with a simulator backend:
    backend = Simulator(rnd_seed=1, gate_fusion=True)
    cache_depth = 10
    rule_set = DecompositionRuleSet(modules=[projectq.setups.decompositions])
    engines = [TagRemover(),
               LocalOptimizer(cache_depth),
               AutoReplacer(rule_set)]
    compiler_engine = MainEngine(backend=Simulator(rnd_seed=1))

    # Initialize the wavefunction
    wavefunction = compiler_engine.allocate_qureg(n_qubit)

    # Apply the circuit
    ansatz(parameter, wavefunction)

    # Use the engine to implement the gates
    compiler_engine.flush()

    # Evaluate the energy and reset wavefunction
    energy = compiler_engine.backend.get_expectation_value(
        hamiltonian, wavefunction)

    # For deallocate qubit
    All(Measure) | wavefunction
    compiler_engine.flush()

    #print(energy,parameter)

    return energy
