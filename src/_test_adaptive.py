from CircuitConstructor import FixedDepthSweepConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_H2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev, \
    jordan_wigner
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool

if __name__ == "__main__":
    """
    Implementation of the paper
    "Short-depth trial-wavefunctions for the variational quantum eigensolver 
    based on the problem Hamiltonian"
    arXiv:1908.09533v1
    """

<<<<<<< HEAD
    mole_name="H2"
    

    basis="6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8),8)
    energy_obj = make_example_H2(basis="6-31g",fermi_qubit_transform=transform,is_computed=False)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])
=======
    mole_name = "H2"
>>>>>>> bea98ac259b1c6050bae9d98f55982906cf3aa72

    basis = "6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8), 8)
    energy_obj = make_example_H2O(basis=basis, fermi_qubit_transform=transform, is_computed=False)
    energy_obj = get_reduced_energy_obj_with_HF_init(energy_obj, [3, 7])

    # Generate the block pool
    # pool1=BlockPool(all_rotation_pool(energy_obj.n_qubit,only_odd_Y_operators=True))
    pool = BlockPool(quasi_imaginary_evolution_rotation_pool(energy_obj.hamiltonian))

    # print(pool)
    # Generate the circuit constructor
<<<<<<< HEAD
    constructor=FixedDepthSweepConstructor(energy_obj,pool,n_max_block=15,project_name="_".join([mole_name,basis]))
=======
    constructor = FixedDepthSweepConstructor(energy_obj, pool, n_max_block=, project_name="_".join([mole_name, basis]))
>>>>>>> bea98ac259b1c6050bae9d98f55982906cf3aa72

    # Run the constructor
    constructor.execute_construction()
