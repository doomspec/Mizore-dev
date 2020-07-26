from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool,all_rotation_pool

if __name__=="__main__":

    """
     Implementation of the adaptive ansatz construction with a pauliword rotation pool described in 
     "Iterative Qubit Coupled Cluster Approach with Efficient Screening of Generators"
     (J. Chem. Theory Comput. 2020, 16, 1055−1063))
    """
    

    # Generate the Hamiltonian
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=bravyi_kitaev)

    # Generate the block pool
    pool=pool=BlockPool(all_rotation_pool(hamiltonian_obj.n_qubit,max_length=hamiltonian_obj.n_qubit))

    # Generate the circuit constructor
    constructor=GreedyConstructor(hamiltonian_obj,pool)

    # Run the constructor
    constructor.start()
    constructor.join()
    
    constructor.terminate()