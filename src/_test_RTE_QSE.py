from CircuitConstructor import FixedDepthSweepConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool
from ParallelTaskRunner import TaskManager
from ParallelTaskRunner import OptimizationTask
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer,RealTimeEvolutionOptimizer
from Blocks import BlockCircuit
import pickle
from MoreMethods._subspace_expansion import *

if __name__ == "__main__":
    """
    Implementation of ansatz-based imaginary time evolution described in npj Quantum Information (2019) 5:75
    (Variational ansatz-based quantum simulation of imaginary time evolution)
    """

    mole_name = "H2"
    basis = "6-31g"
    transform = make_transform_spin_separating(get_parity_transform(8), 8)
    energy_obj = get_example_molecular_hamiltonian(
        "H2", basis=basis, fermi_qubit_transform=transform)
    energy_obj = get_reduced_energy_obj_with_HF_init(energy_obj, [3, 7])

    pool = BlockPool(quasi_imaginary_evolution_rotation_pool(
        energy_obj.hamiltonian))

    n_step=10
    optimizer = ImaginaryTimeEvolutionOptimizer(get_best_result=False, inverse_evolution=False, random_adjust=0.01,
        verbose=True, n_step=n_step, stepsize=1e-2, max_increase_n_step=n_step,fig_path="ITE")
    
    with open("src/H2_5_blocks.bc", "rb") as f:
        circuit: BlockCircuit = pickle.load(f)
    print(circuit.active_position_list)

    for i in range(3):
        op = OptimizationTask(circuit, optimizer, energy_obj.get_cost())
        cost,amp=op.run()
        circuit.adjust_parameter_on_active_position(amp)
        print(cost,amp)
        with open("src/H2_5_blocks_"+str(i)+".bc", "wb") as f:
            pickle.dump(circuit,f)
    
    with open("src/H2_5_blocks.bc", "rb") as f:
        circuit: BlockCircuit = pickle.load(f)
    circuits=[circuit]
    for i in range(3):
        with open("src/H2_5_blocks_"+str(i)+".bc", "rb") as f:
            circuits.append(pickle.load(f))
    for circuit in circuits:
        print(circuit)
    qse_solver=SubspaceExpansionSolver(circuits,energy_obj.hamiltonian)
    qse_solver.execute()
    