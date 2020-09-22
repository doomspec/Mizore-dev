
import numpy as np
import scipy.sparse.linalg as slg
import scipy.linalg as dlg
PauliI = np.array([[1, 0], [0, 1]], np.complex)
PauliX = np.array([[0, 1], [1, 0]], np.complex)
PauliY = np.array([[0, -1j], [1j, 0]], np.complex)
PauliZ = np.array([[1, 0], [0, -1]], np.complex)
P = [PauliI, PauliX, PauliY, PauliZ]
pauli_dict = {"I":PauliI,"X":PauliX,"Y":PauliY, "Z":PauliZ}

def solve_ground_state_energy(energy_obj):
    return solve_ground_state_of_operator(energy_obj.n_qubit,energy_obj.hamiltonian)[0]

def solve_ground_state(energy_obj):
    return solve_ground_state_of_operator(energy_obj.n_qubit,energy_obj.hamiltonian)

def solve_ground_state_of_operator(n_qubit,hamiltonian):
    return solve_ground_state_by_mat(qubit_operator2matrix(n_qubit,hamiltonian))

def solve_ground_state_by_mat(h,nmax=3000):
  """Get a ground state"""
  info = False
  if h.shape[0]>nmax:
    if info: print("Calling ARPACK")
    eig,eigvec = slg.eigsh(h,k=10,which="SA",maxiter=100000)
    eig = np.sort(eig)
  else:
    if info: print("Full diagonalization")
    eig,eigvec = dlg.eigh(h)
  return eig[0],eigvec.transpose()[0]

def qubit_operator2matrix(n_qubit,hamiltonian):
    n_dim = 2**n_qubit
    mat = np.zeros((n_dim, n_dim), complex)
    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            if not string_pauli:
                mat += pauli_and_coff.terms[string_pauli]*np.eye(n_dim)
                continue
            string_pauli_i=0
            if string_pauli[0][0]==0:
                pauli0 = pauli_dict[string_pauli[0][1]]
                string_pauli_i+=1
            else:
                pauli0 = PauliI
            for i in range(1,n_qubit):
                if string_pauli_i==len(string_pauli):
                    pauli0 = np.kron(PauliI,pauli0)
                    continue
                if i == string_pauli[string_pauli_i][0]:
                    pauli0 = np.kron(pauli_dict[string_pauli[string_pauli_i][1]],pauli0)
                    string_pauli_i+=1
                else:
                    pauli0 = np.kron(PauliI,pauli0)
            
            mat += pauli_and_coff.terms[string_pauli]*pauli0
    return mat
    

