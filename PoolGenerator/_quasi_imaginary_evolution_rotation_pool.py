from PoolGenerator._entangler_pool import EntanglerPool
from Entanglers._rotation_entangler import RotationEntangler
from copy import copy

class QuasiImaginaryEvolutionRotationPool(EntanglerPool):
    """Entangler pool inspired by QAOA from arXiv:1908.09533v1.
    The pool consists of the RotationEntangler with Pauli words modified from the Hamiltonian.
    The modification of Pauli words is to replace one Y by X or one X by Y.
    """
    def __init__(self,hamiltonian):
        for pauli_and_coff in hamiltonian.get_operators():
            for string_pauli in pauli_and_coff.terms:
                qsubset,pauli=string_pauli2qsubset_pauli(string_pauli)
                pauli=make_pauli_imaginary(pauli)
                if pauli!=None:
                    self.entanglers.append(RotationEntangler(qsubset,pauli))
    
def string_pauli2qsubset_pauli(string_pauli,make_imaginary=False):
    qsubset=[]
    pauli=[]
    pauli_dict={'X':1,'Y':2,'Z':3}
    for term in string_pauli:
        qsubset.append(term[0])
        pauli.append(pauli_dict[term[1]])
    return qsubset,pauli

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