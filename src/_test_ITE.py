from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_H2O,make_example_LiH
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool
from ParallelTaskRunner import TaskManager
from ParallelTaskRunner import OptimizationTask
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer,RealTimeEvolutionOptimizer
from Blocks import BlockCircuit
import pickle

if __name__ == "__main__":
    """
    Implementation of ansatz-based imaginary time evolution described in npj Quantum Information (2019) 5:75
    (Variational ansatz-based quantum simulation of imaginary time evolution)
    """

    mole_name = "H2"
    basis = "6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8), 8)
    energy_obj = make_example_LiH()
    energy_obj = get_reduced_energy_obj_with_HF_init(energy_obj, [3, 7])


    pool = BlockPool(quasi_imaginary_evolution_rotation_pool(
        energy_obj.hamiltonian))

    task_manager=None#TaskManager(n_processor=1,task_package_size=1000)

    optimizer = ImaginaryTimeEvolutionOptimizer(random_adjust=0.1,task_manager=task_manager,
        verbose=True, n_step=100, stepsize=1e-2, max_increase_n_step=100,fig_path="ITE",inverse_evolution=False)

    with open("src/H2_5_blocks.bc", "rb") as f:
        circuit: BlockCircuit = pickle.load(f)
     
    print(circuit)

    op = OptimizationTask(circuit, optimizer, energy_obj.get_cost())
    
    op.run()
    
