from openfermion.ops import FermionOperator, QubitOperator
from openfermion.transforms import bravyi_kitaev, jordan_wigner
from openfermion.utils import hermitian_conjugated
import numpy as np
from math import sqrt, cos, pi

def AAH_model(L,w,t=2,v=0):
    '''
    Test for MBL, ref PhysRevLett.118.016804
    args: L: the system size
        w: order parameter
        t: hopping strength
        v: interaction strength
    return: fermion hamiltonian of AAH model
    '''
    phi = (1+sqrt(5))/2
    h = []
    # {h_j} are random fields
    for i in range(L):
        alpha = np.random.uniform(0,2*pi)
        h.append(w*cos(2*pi*phi*(i+1)+alpha))

    hamiltonian = FermionOperator()
    for i in range(L-1):
        # hopping
        hamiltonian += FermionOperator((
            (i, 1),
            (i+1, 0)),
            -t/2)
        hamiltonian += FermionOperator((
            (i+1, 1),
            (i, 0)),
            -t/2)
        
        # random field
        hamiltonian += FermionOperator((
            (i, 1),
            (i, 0)),
            h[i])

        # interaction strength
        hamiltonian += FermionOperator((
            (i, 1),
            (i, 0),
            (i+1, 1),
            (i+1, 0)),
            v)
        hamiltonian += FermionOperator((
            (i, 1),
            (i, 0)),
            -v/2)
        hamiltonian += FermionOperator((
            (i+1, 1),
            (i+1, 0)),
            -v/2)

    hamiltonian += FermionOperator((
            (i, 1),
            (i, 0)),
            h[L-1])

    # constant = \sum_{j=1}^L -h_j/2 + (L-1)v/4

    return hamiltonian