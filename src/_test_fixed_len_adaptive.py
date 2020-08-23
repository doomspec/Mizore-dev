from CircuitConstructor import FixedDepthSweepConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool,quasi_imaginary_evolution_rotation_pool,all_rotation_pool
from ParallelTaskRunner import TaskManager
if __name__=="__main__":
    """
    Implementation of the paper
    "Short-depth trial-wavefunctions for the variational quantum eigensolver 
    based on the problem Hamiltonian"
    arXiv:1908.09533v1
    """

    mole_name="H2"
    

    basis="6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8),8)
    energy_obj = get_example_molecular_hamiltonian(
            "H2", basis=basis, fermi_qubit_transform=transform)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])
    """
    basis="sto-3g"
    transform = make_transform_spin_separating(bravyi_kitaev,4)
    energy_obj = get_example_molecular_hamiltonian(
            "H2", basis=basis, fermi_qubit_transform=transform)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[1,3])
    """

    # Generate the block pool
    #pool=BlockPool(all_rotation_pool(hamiltonian_obj.n_qubit,max_length=hamiltonian_obj.n_qubit,only_odd_Y_operators=True))
    pool=BlockPool(quasi_imaginary_evolution_rotation_pool(energy_obj.hamiltonian))

    task_manager=TaskManager(5,5)
    # Generate the circuit constructor
    constructor=FixedDepthSweepConstructor(energy_obj,pool,task_manager=task_manager ,n_max_block=5,sweep_start_position=1,gradient_screening_rate=0.1,project_name="_".join([mole_name,basis]))

    # Run the constructor
    constructor.execute_construction()

    task_manager.close()
