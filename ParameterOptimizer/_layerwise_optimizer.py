from Blocks._block_circuit import BlockCircuit
from ParameterOptimizer._circuit_optimizer import basinhopping_optimizer
from Utilities.Tools import random_list
from Blocks._parametrized_circuit import ParametrizedCircuit


def LayerwiseOptimizer(circuit: BlockCircuit, hamiltonian, random_initial=0.1, niter=10, temperature=0.5):
    # TODO not finished
    _circuit = circuit.duplicate()
    energy = 0
    parameter = []
    for layer in range(len(_circuit.block_list)):
        pcircuit = _circuit.block_list[layer].get_ansatz_by_position_list(
            (layer,))
        energy, block_para = basinhopping_optimizer(
            pcircuit, hamiltonian, random_initial=random_initial, niter=niter, temperature=temperature)
        _circuit.block_list[layer].parameter = block_para
        parameter.extend(block_para)
    return energy, parameter
