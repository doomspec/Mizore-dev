from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool
from Blocks import MultiRotationEntangler,BlockCircuit,HardwareEfficientEntangler
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer

if __name__ == "__main__":

     """
     Implementation of ansatz-based imaginary time evolution described in
     "Variational ansatz-based quantum simulation of imaginary time evolution"
     """

     transform = bravyi_kitaev

     # Generate the Hamiltonian
     hamiltonian_obj = get_example_molecular_hamiltonian(
          "H2", basis="sto-3g", fermi_qubit_transform=transform)

     # Generate the block pool
     pool = BlockPool(MultiRotationEntangler(hamiltonian_obj.hamiltonian))

     init_circuit=BlockCircuit(hamiltonian_obj.n_qubit)
     init_circuit.add_block(hamiltonian_obj.init_block)
     init_circuit.add_block(HardwareEfficientEntangler((0,2)))

     # Generate the circuit constructor
     constructor = GreedyConstructor(hamiltonian_obj, pool, optimizer=ImaginaryTimeEvolutionOptimizer(
          verbose=True, n_step=100, max_increase_n_step=10),init_circuit=init_circuit)

     # Run the constructor
     constructor.start()
     constructor.join()

     constructor.terminate()
