from openfermion.ops import QubitOperator
from HamiltonianGenerator._stationary_qubit_reducer import get_reduced_energy_obj_with_HF_init
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev
from HamiltonianGenerator import make_example_N2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating
from Blocks import MultiRotationEntangler,BlockCircuit,HardwareEfficientEntangler
from Utilities.CircuitEvaluation import get_quantum_engine
from Precalculation.iTensorCore import run_classcal_precalculation
from Utilities.WaveLocalProperties import get_mutual_information_by_2DMs,get_EoF_by_2DMs

transform = make_transform_spin_separating(get_parity_transform(16),16)
energy_obj =make_example_N2(is_computed=False)
energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[11,15])
"""
transform = make_transform_spin_separating(bravyi_kitaev,4)
energy_obj = get_example_molecular_hamiltonian(
        "H2", basis="sto-3g", fermi_qubit_transform=transform)
energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[1,3])
"""
classical_res=run_classcal_precalculation(energy_obj.n_qubit,energy_obj.hamiltonian,calc_2DM=True)
classical_res["MI"]=get_mutual_information_by_2DMs(classical_res["2DM"]).tolist()
classical_res["EoF"]=get_EoF_by_2DMs(classical_res["2DM"]).tolist()
print("Energy",classical_res["energy"])
print("Entropy",classical_res["entropy"])
print("Entanglement of Formation",classical_res["EoF"])
print("Mutual Information",classical_res["MI"])
