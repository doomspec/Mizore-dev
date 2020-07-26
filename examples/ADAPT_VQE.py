from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool, fermion_SD_excitation_multi_parameter_pool

if __name__ == "__main__":
    
    """
    Implementation of the adaptive ansatz construction with a double excitation pool described in 
    "An adaptive variational algorithm for exact molecular simulations on a quantum computer"
    (Nat Commun 10, 3007 (2019))
    """

    transform = bravyi_kitaev

    # Generate the Hamiltonian
    hamiltonian_obj = get_example_molecular_hamiltonian(
        "H2", basis="sto-3g", fermi_qubit_transform=transform)

    # Generate the block pool
    pool = BlockPool(fermion_SD_excitation_multi_parameter_pool(
        hamiltonian_obj.n_qubit, fermi_qubit_transform=transform))

    # Generate the circuit constructor
    constructor = GreedyConstructor(hamiltonian_obj, pool)

    # Run the constructor
    constructor.start()
    constructor.join()
    
    constructor.terminate()
