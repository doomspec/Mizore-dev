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

# This part can easily change to use HiQ. 
# We use projectq here because it can be easily installed by pip and thus easily for Mizore to be installed.


def get_quantum_engine():
    # Create a main compiler engine with a simulator backend:
    backend = Simulator(rnd_seed=1, gate_fusion=True)
    cache_depth = 10
    rule_set = DecompositionRuleSet(modules=[projectq.setups.decompositions])
    engines = [TagRemover(),
               LocalOptimizer(cache_depth),
               AutoReplacer(rule_set)]
    compiler_engine = MainEngine(backend=backend, engine_list=engines)

    return compiler_engine


def evaluate_ansatz_expectation(parameter, n_qubit, hamiltonian, ansatz):
    """
    Args:

    Returns:

    """

    compiler_engine = get_quantum_engine()

    # Initialize the wavefunction
    wavefunction = compiler_engine.allocate_qureg(n_qubit)

    # Apply the circuit
    ansatz(parameter, wavefunction)

    # Use the engine to implement the gates
    compiler_engine.flush()

    # Evaluate the energy
    energy = compiler_engine.backend.get_expectation_value(
        hamiltonian, wavefunction)

    # For deallocate qubit
    All(Measure) | wavefunction
    compiler_engine.flush()

    #print(energy,parameter)

    return energy


def evaluate_ansatz_amplitudes(n_qubit, ansatz, bit_string_list):
    """
    Return the amplitudes of the kets in the bit_string_list
    Each bit_string should be a list of booleans like [False]*n_qubit
    False: |0>; True: |1>
    """
    compiler_engine = get_quantum_engine()

    # Initialize the wavefunction
    wavefunction = compiler_engine.allocate_qureg(n_qubit)

    # Apply the circuit
    ansatz([0]*100, wavefunction)

    # Use the engine to implement the gates
    compiler_engine.flush()

    amp_list = []
    # Evaluate the amplitude
    for bit_string in bit_string_list:
        amp = compiler_engine.backend.get_amplitude(bit_string, wavefunction)
        amp_list.append(amp)

    # For deallocate qubit
    All(Measure) | wavefunction
    compiler_engine.flush()

    return amp_list


def evaluate_ansatz_0000_amplitudes(n_qubit, ansatz):
    return evaluate_ansatz_amplitudes(n_qubit, ansatz, [[False] * n_qubit])[0]