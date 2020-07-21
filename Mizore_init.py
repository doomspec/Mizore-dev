from CircuitConstructor._greedy_constructor import GreedyConstructor
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian,get_maxcut
from PoolGenerator._all_rotation_pool import AllRotationPool
from PoolGenerator._quasi_imaginary_evolution_rotation_pool import QuasiImaginaryEvolutionRotationPool
from PoolGenerator._block_pool import BlockPool
from openfermion.transforms import jordan_wigner
from Blocks._multi_rotation_entangler import MultiRotationEntangler

if __name__=="__main__":

    #hamiltonian,hamiltonian_info=get_maxcut(4)
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",fermi_qubit_transform=jordan_wigner)
    #print(hamiltonian)
    #pool=AllRotationPool(n_qubit,max_length=2)
    pool=QuasiImaginaryEvolutionRotationPool(hamiltonian_obj.hamiltonian)
    #pool=BlockPool(init_block=MultiRotationEntangler(hamiltonian))
    constructor=GreedyConstructor(hamiltonian_obj,pool)
    constructor.start()
    constructor.join()