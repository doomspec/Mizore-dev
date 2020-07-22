from CircuitConstructor import GreedyConstructor
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian,get_maxcut
from PoolGenerator._rotation_pools import all_rotation_pool,quasi_imaginary_evolution_rotation_pool
from PoolGenerator import BlockPool
from openfermion.transforms import jordan_wigner
from Blocks._multi_rotation_entangler import MultiRotationEntangler

if __name__=="__main__":

    hamiltonian_obj=get_maxcut(4)
    #hamiltonian_obj=get_example_molecular_hamiltonian("H2",fermi_qubit_transform=jordan_wigner)
    #print(hamiltonian)
    #pool=AllRotationPool(n_qubit,max_length=2)
    #pool=BlockPool(block_iter=quasi_imaginary_evolution_rotation_pool(hamiltonian_obj.hamiltonian))
    pool=BlockPool(block_iter=all_rotation_pool(hamiltonian_obj.n_qubit,max_length=2))
    #pool=BlockPool(init_block=MultiRotationEntangler(hamiltonian))
    constructor=GreedyConstructor(hamiltonian_obj,pool)
    constructor.start()
    constructor.join()