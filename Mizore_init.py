from CircuitConstructor import GreedyConstructor
from HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian, get_maxcut
from PoolGenerator._rotation_pools import all_rotation_pool, quasi_imaginary_evolution_rotation_pool
from PoolGenerator import BlockPool
from PoolGenerator._fermion_pools import fermion_SD_excitation_multi_parameter_pool,upccgsd_pool
from openfermion.transforms import jordan_wigner,bravyi_kitaev
from HamiltonianGenerator.FermionTransform import get_parity_transform,make_transform_spin_separating
from Blocks._multi_rotation_entangler import MultiRotationEntangler
from Blocks._hardware_efficient_entangler import HardwareEfficientEntangler
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer
if __name__=="__main__":

    fermi_qubit_transform=bravyi_kitaev#make_transform_spin_separating(get_parity_transform(12),12)

    #hamiltonian_obj=get_maxcut(4)
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=fermi_qubit_transform)
    print(hamiltonian_obj.n_qubit)
    #print(hamiltonian)
    #pool=BlockPool(block_iter=quasi_imaginary_evolution_rotation_pool(hamiltonian_obj.hamiltonian))
    #pool=BlockPool(block_iter=all_rotation_pool(hamiltonian_obj.n_qubit,max_length=2))
    #pool=BlockPool(init_block=MultiRotationEntangler(hamiltonian_obj.hamiltonian))
    pool=BlockPool(fermion_SD_excitation_multi_parameter_pool(hamiltonian_obj.n_qubit,fermi_qubit_transform=bravyi_kitaev))
    #pool=BlockPool(init_block=HardwareEfficientEntangler((0,1,2,3)))
    constructor=GreedyConstructor(hamiltonian_obj,pool)
    #optimizer=ImaginaryTimeEvolutionOptimizer()
    constructor.start()
    constructor.join()
    constructor.terminate()
