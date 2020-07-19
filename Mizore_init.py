from CircuitConstructor._greedy_constructor import GreedyConstructor
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian,get_maxcut
from PoolGenerator._all_rotation_pool import AllRotationPool
from PoolGenerator._quasi_imaginary_evolution_rotation_pool import QuasiImaginaryEvolutionRotationPool
from openfermion.transforms import jordan_wigner

if __name__=="__main__":

    hamiltonian,hamiltonian_info=get_maxcut(4)#get_example_molecular_hamiltonian("H2",fermi_qubit_transform=jordan_wigner)
    n_qubit=hamiltonian_info["n_qubit"]
    #print(hamiltonian)
    pool=AllRotationPool(n_qubit,max_length=2)
    #pool=QuasiImaginaryEvolutionRotationPool(hamiltonian)
    constructor=GreedyConstructor(n_qubit,hamiltonian,pool)
    constructor.start()
    constructor.join()