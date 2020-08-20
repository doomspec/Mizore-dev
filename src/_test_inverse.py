from Blocks import Block
from Blocks import BlockCircuit
from Blocks import HardwareEfficientEntangler,RotationEntangler,EfficientCoupledCluster
from copy import copy
from Utilities.Tools import random_list
from Utilities.CircuitEvaluation import evaluate_ansatz_amplitudes

def test_block_inverse(n_qubit,_block:Block):
    for _i in range(10):
        
        circuit=BlockCircuit(n_qubit)
        block=copy(_block)
        circuit.add_block(block)
        block.is_inversed=True
        circuit.add_block(block)
        parameter = random_list(-1, 1, block.n_parameter)
        parameter.extend(parameter)
        circuit.adjust_all_parameter_by_list(parameter)
        #print(circuit)
        #print(circuit.get_ansatz().n_parameter)
        print(abs((evaluate_ansatz_amplitudes(n_qubit,circuit.get_ansatz().ansatz,[[0]*4]))[0]))



if __name__ == "__main__":

    from openfermion.transforms import bravyi_kitaev
    from HamiltonianGenerator import get_example_molecular_hamiltonian
    from Blocks import MultiRotationEntangler,BlockCircuit,HardwareEfficientEntangler

    transform = bravyi_kitaev

    # Generate the Hamiltonian
    hamiltonian_obj = get_example_molecular_hamiltonian(
          "H2", basis="sto-3g", fermi_qubit_transform=transform)

    block=EfficientCoupledCluster((0,1,2,3))
    #block=MultiRotationEntangler(hamiltonian_obj.hamiltonian)
    test_block_inverse(4,block)



