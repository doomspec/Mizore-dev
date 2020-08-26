from MoreMethods._subspace_expansion import *
import pickle
from Blocks import BlockCircuit,CompositiveBlock
from HamiltonianGenerator.TestHamiltonian import make_example_H2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from MoreMethods._Krylov_algorithm import *

if __name__ == "__main__":
    with open("src/H2_5_blocks_1.bc", "rb") as f:
        circuit:BlockCircuit = pickle.load(f)

    mole_name="H2"
    

    basis="6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8),8)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])

    #circuits=get_growing_circuit_list(circuit)
    circuits=generate_Krylov_circuits(energy_obj.hamiltonian,0.01,3,CompositiveBlock(circuit))#energy_obj.init_block)
    qse_solver=SubspaceExpansionSolver(circuits,energy_obj.hamiltonian)
    qse_solver.execute()
    

    
