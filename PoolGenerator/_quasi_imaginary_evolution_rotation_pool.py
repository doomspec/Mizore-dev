from PoolGenerator._block_pool import BlockPool
from Blocks._rotation_entangler import RotationEntangler
from copy import copy
from Utilities.Iterators import iter_qsubset_pauli_of_operator
class QuasiImaginaryEvolutionRotationPool(BlockPool):
    """Entangler pool inspired by QAOA from arXiv:1908.09533v1.
    The pool consists of the RotationEntangler with Pauli words modified from the Hamiltonian.
    The modification of Pauli words is to replace one Y by X or one X by Y.
    """
    def __init__(self,hamiltonian):
        for qsubset,pauli in iter_qsubset_pauli_of_operator(hamiltonian):
                pauli=make_pauli_imaginary(pauli)
                if pauli!=None:
                    self.blocks.append(RotationEntangler(qsubset,pauli))
    

def make_pauli_imaginary(pauli):
    """
    Modify the Pauli word by replacing one Y by X or one X by Y.
    Return the modified Pauli word.
    """
    new_pauli=copy(pauli)
    for i in range(len(pauli)):
        if new_pauli[i]==1:
            new_pauli[i]=2
            return new_pauli
        if new_pauli[i]==2:
            new_pauli[i]=1
            return new_pauli
    return None