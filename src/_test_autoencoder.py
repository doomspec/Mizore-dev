
import pickle
from Blocks import BlockCircuit,HardwareEfficientEntangler
from Blocks._pauli_gates_block import PauliGatesBlock
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init

if __name__ == "__main__":
    a=set([1,2,3,4,5])
    b=[1321,352,123,534]
    b.pop(1)
    print(b)