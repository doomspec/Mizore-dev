from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool,all_rotation_pool

if __name__=="__main__":

    """
    Implementation of ansatz-based imaginary time evolution described in
    "Variational ansatz-based quantum simulation of imaginary time evolution"
    on the Hamiltonian-based ansatz described in
    "Improving the accuracy of quantum computational chemistry using the transcorrelated method"
    (arXiv:2006.11181v1)cd 
    """

    # Generate the Hamiltonian
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=bravyi_kitaev)

    # Generate the exponentiated pauliword e^(iPt) block pool
    pool=BlockPool(all_rotation_pool(hamiltonian_obj.n_qubit,max_length=hamiltonian_obj.n_qubit))

    # Generate the circuit constructor
    constructor=GreedyConstructor(hamiltonian_obj,pool)

    # Run the constructor
    constructor.start()
    constructor.join()
    constructor.terminate()
