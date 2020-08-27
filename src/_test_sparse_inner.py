from Blocks._sparse_circuit_utilities import get_inner_product_task_on_sparse_circuit,get_localized_circuit,get_0000_amplitude_on_sparse_circuit
from Blocks import BlockCircuit,HardwareEfficientEntangler,HartreeFockInitBlock,RotationEntangler,PauliGatesBlock


if __name__=="__main__":
    bc3=BlockCircuit(6)
    bc3.add_block(RotationEntangler((0,1,2),(3,1,1),init_angle=0.5))
    bc3.add_block(PauliGatesBlock([(1,'Z'),(2,'Z'),(3,'Z')]))
    bc3.add_block(RotationEntangler((3,4,5),(1,1,1),init_angle=1))


    from Utilities.CircuitEvaluation import evaluate_ansatz_0000_amplitudes

    print(get_0000_amplitude_on_sparse_circuit(bc3))
    print(evaluate_ansatz_0000_amplitudes(6,bc3.get_ansatz_on_active_position().ansatz))