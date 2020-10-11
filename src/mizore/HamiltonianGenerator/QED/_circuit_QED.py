from openfermion.ops import FermionOperator, QubitOperator, BosonOperator
from openfermion.transforms import bravyi_kitaev, jordan_wigner
from openfermion.utils import hermitian_conjugated
import numpy as np
from math import sqrt, cos, pi

def Jaynes_Cummings_model(ogr,oga,g): #TODO
    '''
    matter-light interaction
    args:
        ogr: resonance frequency of the cavity
        oga: transition frequency
        g: electric dipolar coupling

    '''
    hamiltonian = FermionOperator()
    # cavity term
    hamiltonian += BosonOperator((
        (1, 1),
        (1, 0)),
        ogr)
    # atomic term
    hamiltonian += 0.5*ogr*QubitOperator('Z0')
    # interaction term
    hamiltonian += BosonOperator((1, 0),g)*(FermionOperator((0, 1),1))+BosonOperator((1, 1),g)*(FermionOperator((0, 0),1))

    return hamiltonian

print(Jaynes_Cummings_model(1,1,1))