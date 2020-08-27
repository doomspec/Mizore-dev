from MoreMethods._subspace_expansion import *
import pickle
from Blocks import BlockCircuit
from HamiltonianGenerator.FermionTransform import make_transform_spin_separating,get_parity_transform,bravyi_kitaev
from HamiltonianGenerator import get_reduced_energy_obj_with_HF_init
from MoreMethods._Krylov_algorithm import *
if __name__ == "__main__":
    a=set([1,2,3])
    b=set([3,4,5])
    a.update(b)
    print(a)
    