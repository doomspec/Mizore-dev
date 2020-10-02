from CircuitConstructor import FixedDepthSweepConstructor, GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_H2
from Blocks import BlockCircuit, HartreeFockInitBlock
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev, \
    jordan_wigner
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool
from ParallelTaskRunner import TaskManager

from gauge import get_coverage, get_parameter_efficiency

mole_name="H2"

basis="sto-3g"
transform = jordan_wigner
energy_obj = make_example_H2(basis=basis,fermi_qubit_transform=transform,is_computed=False)
#energy_obj=get_reduced_energy_obj_with_HF_init(energy_obj,[3,7])

# Generate the block pool
pool=BlockPool(all_rotation_pool(energy_obj.n_qubit,only_odd_Y_operators=True))
# pool = BlockPool(quasi_imaginary_evolution_rotation_pool(energy_obj.hamiltonian))

# print(pool)
# Generate the circuit constructor
#init=BlockCircuit(4)
#init.add_block(HartreeFockInitBlock([0,1]))
constructor=GreedyConstructor(
    energy_obj, pool, project_name="_".join([mole_name,basis]), task_manager=TaskManager(n_processor=4))

# Run the constructor
#bc = constructor.execute_construction()
bc = constructor.run()
print(bc)
bc.remove_block(0)

state_init = '0000'
state_j = '1100'
#print(get_coverage(bc, state_init, state_j))
print(get_parameter_efficiency(bc, state_init))