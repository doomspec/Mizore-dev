from openfermion.ops import QubitOperator
import numpy as np
import math
PauliI_half = np.array([[0.5, 0], [0, 0.5]], np.complex)
PauliI = np.array([[1, 0], [0, 1]], np.complex)
PauliX = np.array([[0, 1], [1, 0]], np.complex)
PauliY = np.array([[0, -1j], [1j, 0]], np.complex)
PauliZ = np.array([[1, 0], [0, -1]], np.complex)
PauliMat = [PauliI, PauliX, PauliY, PauliZ]
PauliString = ['I', 'X', 'Y', 'Z']

def get_one_DM(get_expectation_value, wavefunction):
    n_qubit = len(wavefunction)
    one_DMs = np.array([PauliI]*n_qubit)
    for i in range(0, n_qubit):
        for ip in range(1, 4):
            one_DMs[i] = one_DMs[i]+get_expectation_value(
                QubitOperator(PauliString[ip]+str(0)), [wavefunction[i]])*PauliMat[ip]
        one_DMs[i] = one_DMs[i]/2
    return one_DMs

def get_two_density_matrix(get_expectation_value, wavefunction):
    n_qubit = len(wavefunction)
    two_DMs = np.array([[np.kron(PauliI, PauliI)]*n_qubit]*n_qubit)
    for i in range(0, n_qubit):
        for j in range(0, i):
            for ip in range(0, 4):
                for jp in range(0, 4):
                    if ip == 0 and jp == 0:
                        continue
                    if ip == 0:
                        itr_pauli_operator = QubitOperator(
                            PauliString[jp]+str(j))
                    if jp == 0:
                        itr_pauli_operator = QubitOperator(
                            PauliString[ip]+str(i))
                    if ip != 0 and jp != 0:
                        itr_pauli_operator = QubitOperator(
                            PauliString[ip]+str(i)+' '+PauliString[jp]+str(j))
                    two_DMs[i][j] = two_DMs[i][j]+get_expectation_value(
                        itr_pauli_operator, wavefunction)*np.kron(PauliMat[ip], PauliMat[jp])
            two_DMs[i][j] = two_DMs[i][j]/4
    return two_DMs

def two_DM_to_one_DMs(two_DMs):
    one_DM_1=np.array([[0.0+0.0j]*2]*2)
    one_DM_2=np.array([[0.0+0.0j]*2]*2)
    one_DM_1[0][0]=two_DMs[0][0]+two_DMs[1][1]
    one_DM_1[1][0]=two_DMs[2][0]+two_DMs[3][1]
    one_DM_1[0][1]=two_DMs[0][2]+two_DMs[1][3]
    one_DM_1[1][1]=two_DMs[2][2]+two_DMs[3][3]

    one_DM_2[0][0]=two_DMs[0][0]+two_DMs[2][2]
    one_DM_2[1][0]=two_DMs[0][1]+two_DMs[2][3]
    one_DM_2[0][1]=two_DMs[1][0]+two_DMs[3][2]
    one_DM_2[1][1]=two_DMs[1][1]+two_DMs[3][3]
    return one_DM_1,one_DM_2

def entropy_one_DM(one_DM: np.array, test=0):
    eigv = np.linalg.eigvalsh(one_DM)
    #print(eigv)
    realeigv = np.round(np.real(eigv), 7)  # Round
    # print(eigv)
    if test == 1:
        print('eigv', realeigv)
    norm = 0
    for i in range(0, len(one_DM[0])):
        norm += realeigv[i]
    if norm == 0:
        print('Density matrix not proper, eigenvalue sum to 0, 0 returned')
        return 0
    else:
        realeigv = realeigv/norm
        if test == 1:
            print('norm', norm)

    entropy = 0
    for i in range(0, len(one_DM[0])):
        if realeigv[i] != 0 and realeigv[i] != 1:
            if realeigv[i]>0:
                entropy += -realeigv[i]*math.log2(realeigv[i])
            else:
                print("problem")
                #print(one_DM)
    if test == 1:
        print('entropy', entropy)
    return entropy

def get_mutual_information_by_2DMs(two_DMs):
    n_qubit = len(two_DMs)
    mutual_information = np.array([[0.0]*n_qubit]*n_qubit)
    for i in range(0, n_qubit):
        for j in range(0, i):
            one_DM_1,one_DM_2=two_DM_to_one_DMs(two_DMs[i][j])
            mutual_information[i][j] = 0.5*(entropy_one_DM(one_DM_1)+entropy_one_DM(one_DM_2)-entropy_one_DM(two_DMs[i][j]))
            mutual_information[j][i] = mutual_information[i][j]
    return mutual_information