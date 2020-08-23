# Add the root path of the dmrgpy library
import os ; import sys ; sys.path.append(os.getcwd()+'/../../src')
import numpy as np
from dmrgpy import spinchain,multioperator
from openfermion.ops import QubitOperator
from Utilities.WaveLocalProperties import two_DM_to_one_DMs,entropy_one_DM

MAX_N_QUBIT=40
PauliX_MO = [2*multioperator.obj2MO([["Sx",i]]) for i in range(MAX_N_QUBIT)]
PauliY_MO = [2*multioperator.obj2MO([["Sy",i]]) for i in range(MAX_N_QUBIT)]
PauliZ_MO = [2*multioperator.obj2MO([["Sz",i]]) for i in range(MAX_N_QUBIT)]
PauliMO=[None,PauliX_MO,PauliY_MO,PauliZ_MO]

MatI = np.array([[1, 0], [0, 1]], np.complex)
MatX = np.array([[0, 1], [1, 0]], np.complex)
MatY = np.array([[0, -1j], [1j, 0]], np.complex)
MatZ = np.array([[1, 0], [0, -1]], np.complex)
PauliMat = [MatI, MatX, MatY, MatZ]
PauliChar = ['I', 'X', 'Y', 'Z']

def get_one_two_density_matrix(n_qubit,spinchain):
    twodensity = np.array([[np.kron(MatI, MatI)]*n_qubit]*n_qubit)
    onedensity = [MatI]*n_qubit
    for i in range(0, n_qubit):
        for ip in range(1, 4):
            onedensity[i]=onedensity[i]+spinchain.vev(PauliMO[ip][i])*PauliMat[ip]
        onedensity[i]/=2
        #print(onedensity[i])
        for j in range(0, i):
            for ip in range(0, 4):
                for jp in range(0, 4):
                    itr_pauli_operator=0
                    if ip == 0 and jp == 0:
                        continue
                    if ip == 0:
                        itr_pauli_operator = PauliMO[jp][j]
                    if jp == 0:
                        itr_pauli_operator = PauliMO[ip][i]
                    if ip != 0 and jp != 0:
                        itr_pauli_operator = PauliMO[jp][j]*PauliMO[ip][i]
                    twodensity[i][j] = twodensity[i][j]+spinchain.vev(itr_pauli_operator)*np.kron(PauliMat[ip], PauliMat[jp])  
            twodensity[i][j] = twodensity[i][j]/4
            #print(i,j,twodensity[i][j])
            twodensity[j][i]=twodensity[i][j]
    return onedensity,twodensity

def run_classcal_precalculation(n_qubit,hamiltonian:QubitOperator,calc_2DM=False):
    spins = ["S=1/2" for i in range(n_qubit)]
    sc = spinchain.Spin_Chain(spins)
    dmrgpy_hamiltonian=QubitOperator2DmrgpyOperator(n_qubit,hamiltonian)
    #print(dmrgpy_hamiltonian.op)
    sc.set_hamiltonian(dmrgpy_hamiltonian)
    gs_energy=sc.gs_energy(mode="ED")
    ed_obj=sc.get_ED_obj()
    
    if not calc_2DM:
        return gs_energy
    else:
        res={}
        res["energy"]=gs_energy
        one_DM,two_DM=get_one_two_density_matrix(n_qubit,ed_obj)
        res["2DM"]=two_DM
        res["1DM"]=one_DM
        entropy=[entropy_one_DM(one_DM[i]) for i in range(n_qubit)]
        res["entropy"]=entropy
        return res

def QubitOperator2DmrgpyOperator(n_qubit,hamiltonian:QubitOperator):
    dmrgpy_hamiltonian=0
    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            coff=pauli_and_coff.terms[string_pauli]
            ops=coff
            for term in string_pauli:
                if term[1]=="Z":
                    ops=ops*PauliZ_MO[term[0]]
                if term[1]=="Y":
                    ops=ops*PauliY_MO[term[0]]
                if term[1]=="X":
                    ops=ops*PauliX_MO[term[0]]
            dmrgpy_hamiltonian=dmrgpy_hamiltonian+ops
    return dmrgpy_hamiltonian