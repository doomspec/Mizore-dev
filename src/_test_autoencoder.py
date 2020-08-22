from MoreMethods._subspace_expansion import *
import pickle
from Blocks import BlockCircuit
from HamiltonianGenerator import get_example_molecular_hamiltonian
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from MoreMethods._Krylov_algorithm import *
if __name__ == "__main__":
    with open("mizore_results/contruction_runs/H2_6-31g_08-21-00h31m26s/circuit.bc", "rb") as f:
        circuit:BlockCircuit = pickle.load(f)
    mole_name="H2"
    basis="6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8),8)
    energy_obj = get_example_molecular_hamiltonian(
            "H2", basis=basis, fermi_qubit_transform=transform)
    energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])
    
    