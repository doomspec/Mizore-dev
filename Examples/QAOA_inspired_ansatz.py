from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool,quasi_imaginary_evolution_rotation_pool

if __name__=="__main__":
    
    """
    Implementation of the paper
    "Short-depth trial-wavefunctions for the variational quantum eigensolver 
    based on the problem Hamiltonian"
    arXiv:1908.09533v1
    """

    # Generate the Hamiltonian
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="6-31g",fermi_qubit_transform=bravyi_kitaev)

    # Generate the block pool
    pool=pool=BlockPool(quasi_imaginary_evolution_rotation_pool(hamiltonian_obj.hamiltonian))

    # Generate the circuit constructor
    constructor=GreedyConstructor(hamiltonian_obj,pool)

    # Run the constructor
    constructor.start()
    constructor.join()
    
    constructor.terminate()