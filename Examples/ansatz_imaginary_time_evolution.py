from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool
from Blocks import MultiRotationEntangler
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer

if __name__=="__main__":

     """
    Implementation of the adaptive ansatz construction with a pauliword rotation pool described in 
    "Iterative Qubit Coupled Cluster Approach with Efficient Screening of Generators"
    (J. Chem. Theory Comput. 2020, 16, 1055−1063))
    """

    transform=bravyi_kitaev

    # Generate the Hamiltonian
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=transform)

    # Generate the block pool
    pool=BlockPool(MultiRotationEntangler(hamiltonian_obj.hamiltonian))

    # Generate the circuit constructor
    constructor=GreedyConstructor(hamiltonian_obj,pool,optimizer=ImaginaryTimeEvolutionOptimizer())

    # Run the constructor
    constructor.start()
    constructor.join()
    
    constructor.terminate()