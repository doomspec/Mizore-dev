from Blocks import BlockCircuit
import numpy as np
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._pauli_gates_block import PauliGatesBlock
from scipy.linalg import eigh

class SubspaceExpansionSolver:

    def __init__(self,circuit_list,hamiltonian):
        self.circuit_list=circuit_list
        self.n_basis=len(self.circuit_list)
        self.S_mat=np.array([[0.0]*self.n_basis]*self.n_basis,dtype=complex)
        self.H_mat=np.array([[0.0]*self.n_basis]*self.n_basis,dtype=complex)
        self.hamiltonian=hamiltonian
        self.eigvals=None
        self.eigvecs=None
        self.ground_energy=None
        self.ground_state=None
        return

    def execute(self):
        print("Subspace Expansion Method Started")
        print("Calculating S matrix")
        self.calc_S_mat()
        print("Calculating H matrix")
        self.calc_H_mat()
        #print(self.H_mat)
        #print(self.S_mat)
        self.eigvals, self.eigvecs = eigh(self.H_mat, self.S_mat, eigvals_only=False)
        self.ground_energy=self.eigvals[0]
        self.ground_state=self.eigvecs[0]   
        print("The ground state energy is", self.ground_energy)
        print("It's eigenvector is", self.ground_state)

    def calc_H_mat(self):
        for i in range(self.n_basis):
            for j in range(i,self.n_basis):
                h=get_hamiltonian_overlap(self.circuit_list[i],self.circuit_list[j],self.hamiltonian)
                #print(i,j,h)
                self.H_mat[i][j]=h
                self.H_mat[j][i]=np.conjugate(h)
        return

    def calc_S_mat(self):
        for i in range(self.n_basis):
            for j in range(i,self.n_basis):
                if i==j:
                    self.S_mat[i][j]=1.0
                    continue
                s=get_inner_two_circuit_product(self.circuit_list[i],self.circuit_list[j])
                #print(i,j,s)
                self.S_mat[i][j]=s
                self.S_mat[j][i]=np.conjugate(s)
        return

def get_hamiltonian_overlap(first_circuit: BlockCircuit, second_circuit: BlockCircuit, hamiltonian):
    temp_circuit=first_circuit.duplicate()
    overlap=0
    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            temp_circuit.add_block(PauliGatesBlock(string_pauli))
            overlap+=pauli_and_coff.terms[string_pauli]*get_inner_two_circuit_product(temp_circuit,second_circuit)
            temp_circuit.block_list.pop(len(temp_circuit.block_list)-1)
    return overlap

def get_growing_circuit_list(circuit:BlockCircuit):
    new_circuit=circuit.duplicate()
    circuits=[new_circuit]
    n_blocks=len(new_circuit.block_list)
    for i in range(n_blocks):
        new_circuit=new_circuit.duplicate()
        new_circuit.block_list.pop(n_blocks-1-i)
        circuits.append(new_circuit)
    return circuits
