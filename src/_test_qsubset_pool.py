from PoolGenerator._qsubset_pools import get_qsubset_pool_reduced_block_pool,get_hamiltonian_qsubset_pool,number2qsubset,qsubset2number
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from Blocks import MultiRotationEntangler,BlockCircuit,HardwareEfficientEntangler
from PoolGenerator._rotation_pools import all_rotation_pool
from PoolGenerator import BlockPool
from CircuitConstructor import GreedyConstructor

transform = bravyi_kitaev

# Generate the Hamiltonian
hamiltonian_obj = get_example_molecular_hamiltonian(
        "H2", basis="6-31g", fermi_qubit_transform=transform)

qsubsets=get_hamiltonian_qsubset_pool(hamiltonian_obj.hamiltonian)
from Blocks._hardware_efficient_entangler import iter_H_E_entangler_by_qsubsets
pool=BlockPool(iter_H_E_entangler_by_qsubsets(qsubsets))

print(pool)
constructor=GreedyConstructor(hamiltonian_obj,pool)

# Run the constructor
constructor.start()
constructor.join()

constructor.terminate()
