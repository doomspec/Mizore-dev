from SubspaceSolver._subspace_solver import *
import pickle
from Blocks import BlockCircuit, CompositiveBlock
from HamiltonianGenerator.TestHamiltonian import make_example_H2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev, \
    jordan_wigner
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from SubspaceSolver._krylov_algorithm import *
from SubspaceSolver._subspace_constructor import *

if __name__ == "__main__":
    pass

if __name__ == "__main__":
    with open("src/H2_5_blocks.bc", "rb") as f:
        circuit: BlockCircuit = pickle.load(f)

    mole_name = "H2"
    basis = "6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8), 8)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform, is_computed=False)
    energy_obj = get_reduced_energy_obj_with_HF_init(energy_obj, [3, 7])
    # print(energy_obj.hamiltonian)
    """
    basis="sto-3g"
    transform = jordan_wigner#make_transform_spin_separating(bravyi_kitaev,4)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform)
    #energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[1,3])
    """
    circuit = BlockCircuit(energy_obj.n_qubit)
    circuit.add_block(energy_obj.init_block)
    community = [[5, 4], [3, 2, 1, 0]]
    task_manager = TaskManager(n_processor=5, task_package_size=10)
    local_hamiltonian = energy_obj.hamiltonian  # get_reduced_energy_obj_with_HF_init(energy_obj,[5,4],relabel_qubits=False).hamiltonian
    circuits = generate_krylov_circuits(circuit, local_hamiltonian, 0.01, 2)  # energy_obj.init_block)
    # circuits=add_local_complete_basis(circuits,[4,5])

    qse_solver = SubspaceSolver(circuits, energy_obj.hamiltonian, task_manager=task_manager, sparse_circuit=False,
                                progress_bar=True)
    qse_solver.execute()

    task_manager.close()
