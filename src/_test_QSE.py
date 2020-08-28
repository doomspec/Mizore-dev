

if __name__ == "__main__0":
    import pickle
    from Blocks import BlockCircuit,CompositiveBlock
    from HamiltonianGenerator.TestHamiltonian import make_example_H2
    from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
    from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
    from SubspaceExpansion import generate_krylov_circuits,SubspaceExpansionSolver
    with open("src/H2_5_blocks_1.bc", "rb") as f:
        circuit:BlockCircuit = pickle.load(f)

    

    #circuits=get_growing_circuit_list(circuit)
    task_manager=TaskManager(n_processor=4,task_package_size=10)

    circuits=generate_krylov_circuits(energy_obj.hamiltonian,0.01,3,CompositiveBlock(circuit))#energy_obj.init_block)
    qse_solver=SubspaceExpansionSolver(circuits,energy_obj.hamiltonian,task_manager=task_manager)
    qse_solver.execute()

    task_manager.close()

from HamiltonianGenerator import make_example_H2
from Blocks import BlockCircuit

energy_obj=make_example_H2()
init_bc=BlockCircuit(4,init_block=energy_obj.init_block)
from SubspaceExpansion import generate_krylov_circuits
delta_t=0.01
n_circuit=3
krylov_circuits=generate_krylov_circuits(init_bc,energy_obj.hamiltonian,delta_t,n_circuit)

from SubspaceExpansion import SubspaceExpansionSolver

qse_solver=SubspaceExpansionSolver(krylov_circuits,energy_obj.hamiltonian,progress_bar=True)

qse_solver.execute()

    
