from CircuitConstructor import FixedDepthSweepConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import make_example_H2
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating, get_parity_transform, bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from PoolGenerator import BlockPool, quasi_imaginary_evolution_rotation_pool, all_rotation_pool
from ParallelTaskRunner import TaskManager
from ParallelTaskRunner import OptimizationTask
from ParameterOptimizer import ImaginaryTimeEvolutionOptimizer,RealTimeEvolutionOptimizer
from Blocks import BlockCircuit, HardwareEfficientEntangler, RotationEntangler, MultiRotationEntangler
import pickle
from SubspaceSolver._subspace_solver import *
from ParameterOptimizer import BasinhoppingOptimizer
if __name__ == "__main__":
    """
    Implementation of ansatz-based imaginary time evolution described in npj Quantum Information (2019) 5:75
    (Variational ansatz-based quantum simulation of imaginary time evolution)
    """

    mole_name = "H2"
    basis = "sto-3g"
    transform = make_transform_spin_separating(get_parity_transform(4), 4)
    energy_obj = make_example_H2(basis=basis, fermi_qubit_transform=transform)
    energy_obj = get_reduced_energy_obj_with_HF_init(energy_obj, [1, 3])

    n_step=100
    #optimizer = optimizer=BasinhoppingOptimizer(random_initial=0.1)
    optimizer = ImaginaryTimeEvolutionOptimizer(get_best_result=False, inverse_evolution=False, random_adjust=0.01, verbose=True, n_step=n_step, stepsize=1e-1, max_increase_n_step=n_step,fig_path="RTE2")

    circuit=BlockCircuit(2)
    circuit.add_block(MultiRotationEntangler(energy_obj.hamiltonian))
    """
    circuit.add_block(RotationEntangler([0,1],(1,1)))
    circuit.add_block(RotationEntangler([0],(3,)))
    circuit.add_block(RotationEntangler([0,1],(3,3)))
    circuit.add_block(RotationEntangler([1],(3,)))
    """
    circuit.add_block(HardwareEfficientEntangler((0,1)))
    #circuit.add_block(HardwareEfficientEntangler((0,1)))
    #circuit.add_block(HardwareEfficientEntangler((0,1)))
    circuit.set_all_block_active()
    n_para=circuit.count_n_parameter_on_active_position()
    circuit.adjust_parameter_on_active_position([4]*n_para)
    op = OptimizationTask(circuit, optimizer, energy_obj.get_cost())
    print(op.run())
    """
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
    qse_solver=SubspaceSolver(circuits,energy_obj.hamiltonian)
    qse_solver.execute()
    """