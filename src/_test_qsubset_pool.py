from PoolGenerator._qsubset_pools import get_qsubset_pool_reduced_block_pool, get_operator_qsubset_pool, number2qsubset, \
    qsubset2number, iter_entangler_by_qsubsets
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_N2
from Blocks import MultiRotationEntangler, BlockCircuit, HardwareEfficientEntangler
from Blocks._efficient_coupled_cluster import EfficientCoupledCluster
from PoolGenerator._rotation_pools import all_rotation_pool
from PoolGenerator import BlockPool
from CircuitConstructor import GreedyConstructor

transform = bravyi_kitaev

# Generate the Hamiltonian
energy_obj = get_example_molecular_hamiltonian(
    "H2", basis="sto-3g", fermi_qubit_transform=transform)

qsubsets = get_operator_qsubset_pool(energy_obj.hamiltonian)
pool = BlockPool(iter_entangler_by_qsubsets(
    qsubsets, EfficientCoupledCluster))

print(pool)
constructor = GreedyConstructor(energy_obj, pool)

# Run the constructor
constructor.start()
constructor.join()

constructor.terminate()
