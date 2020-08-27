from SubspaceExpansion._subspace_expansion import *
import pickle
from Blocks import BlockCircuit,CompositiveBlock
from HamiltonianGenerator.TestHamiltonian import make_example_H2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev,jordan_wigner
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from SubspaceExpansion._krylov_algorithm import *
from SubspaceExpansion._subspace_constructor import *
if __name__ == "__main__":
    pass

if __name__ == "__main__":

    """
    with open("src/H2_5_blocks.bc", "rb") as f:
        circuit:BlockCircuit = pickle.load(f)

    mole_name="H2"
    basis="6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8),8)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])
    """
    basis="sto-3g"
    transform = jordan_wigner#make_transform_spin_separating(bravyi_kitaev,4)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform)
    #energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[1,3])

    #circuits=get_growing_circuit_list(circuit)
    task_manager=TaskManager(n_processor=10,task_package_size=5)

    #circuits=generate_krylov_circuits(circuit,energy_obj.hamiltonian,0.01,5)#energy_obj.init_block)
    circuits=generate_local_complete_space(BlockCircuit(energy_obj.n_qubit),[0,1,2,3])
    qse_solver=SubspaceExpansionSolver(circuits,energy_obj.hamiltonian,task_manager=task_manager,progress_bar=True)
    qse_solver.execute()

    task_manager.close()