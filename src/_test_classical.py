from openfermion.ops import QubitOperator
from HamiltonianGenerator._stationary_qubit_reducer import get_reduced_energy_obj_with_HF_init
from openfermion.transforms import bravyi_kitaev,jordan_wigner
from HamiltonianGenerator import get_example_molecular_hamiltonian
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating
from Blocks import MultiRotationEntangler,BlockCircuit,HardwareEfficientEntangler
from Utilities.CircuitEvaluation import get_quantum_engine
from Precalculation.iTensorCore import run_classcal_precalculation
from Utilities.WaveLocalProperties import get_mutual_information_by_2DMs,get_EoF_by_2DMs

transform = jordan_wigner#make_transform_spin_separating(bravyi_kitaev,8)
energy_obj = get_example_molecular_hamiltonian(
        "H2", basis="6-31g", fermi_qubit_transform=transform)
energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[])
"""
transform = make_transform_spin_separating(bravyi_kitaev,4)
energy_obj = get_example_molecular_hamiltonian(
        "H2", basis="sto-3g", fermi_qubit_transform=transform)
energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[1,3])
"""
classical_res=run_classcal_precalculation(energy_obj.n_qubit,energy_obj.hamiltonian,calc_2DM=True)
classical_res["MI"]=get_mutual_information_by_2DMs(classical_res["2DM"]).tolist()
classical_res["EoF"]=get_EoF_by_2DMs(classical_res["2DM"]).tolist()
print(classical_res["EoF"])
print(classical_res["MI"])
