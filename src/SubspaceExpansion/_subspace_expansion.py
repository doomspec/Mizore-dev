from Blocks import BlockCircuit
import numpy as np
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._pauli_gates_block import PauliGatesBlock
from scipy.linalg import eigh
from ParallelTaskRunner import TaskManager
from ParallelTaskRunner._inner_product_task import InnerProductTask
from tqdm import tqdm


class SubspaceExpansionSolver:
    """
    The class for Quantum Subspace Expansion (QSE) method, which is also call Quantum Subspace Diagonalization (QSD),
    as in "A non-orthogonal variational quantum eigensolver" (New Journal of Physics, Volume 22, July 2020)
    This methods takes a set of quantum states Psi={|psi_i>} that can be produced by known quantum circuit and 
    diagonalize the Hamiltonian in the space spanned by the set Psi.
    The core procedure is to solve the generalized eigenvalue problem
    Hc=ScE, where H_{ij}=<psi_i|H|psi_j>, S_{ij}=<psi_i|psi_j>, E is the eigenvalue and c is the eigenvector
    The terms can be evaluated efficiently by quantum computers.
    The main problem is how to construct the subspace.
    Attributes:
        circuit_list: the list of circuits produce the state set Psi
        hamiltonian: the objective hamiltonian
        S_mat, H_mat: will be generated after execute()
        eigvals, eigvecs, ground_energy, ground_state will all be generated after execute
    """

    def __init__(self, circuit_list, hamiltonian, task_manager=None, progress_bar=False, sparse_circuit=False):
        self.circuit_list = circuit_list
        self.task_manager = task_manager
        self.progress_bar = progress_bar
        self.sparse_circuit = sparse_circuit
        self.n_basis = len(self.circuit_list)
        self.S_mat = np.array([[0.0]*self.n_basis]*self.n_basis, dtype=complex)
        self.H_mat = np.array([[0.0]*self.n_basis]*self.n_basis, dtype=complex)
        self.hamiltonian = hamiltonian
        self.eigvals = None
        self.eigvecs = None
        self.ground_energy = None
        self.ground_state = None
        return

    def execute(self):
        print("Subspace Expansion Method Started")
        print("Calculating S matrix")
        self.calc_S_mat()
        print("Calculating H matrix")
        self.calc_H_mat()
        # print(self.H_mat)
        # print(self.S_mat)
        self.eigvals, self.eigvecs = eigh(
            self.H_mat, self.S_mat, eigvals_only=False)
        self.ground_energy = self.eigvals[0]
        self.ground_state = self.eigvecs[:,0]
        print("The ground state energy is", self.ground_energy)
        print("It's eigenvector is", self.ground_state)
    
    def calc_H_mat(self):
        if self.task_manager!=None:
            self._calc_H_mat_parellel()
        else:
            self._calc_H_mat_0()

    def _calc_H_mat_0(self):

        if self.progress_bar:
            pbar = tqdm(total=(self.n_basis+1)*self.n_basis//2)
            pbar.set_description(str("H matrix"))
        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                h = get_hamiltonian_overlap_0(
                    self.circuit_list[i], self.circuit_list[j], self.hamiltonian)
                self.H_mat[i][j] = h
                self.H_mat[j][i] = np.conjugate(h)
                if self.progress_bar:
                    pbar.update(1)
        if self.progress_bar:
            pbar.close()
        return

    def _calc_H_mat_parellel(self):
        if self.progress_bar:
            pbar = tqdm(total=(self.n_basis+1)*self.n_basis//2)
            pbar.set_description(str("H matrix"))
        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                task_series_id=str(id(self)%10000)+"i"+str(i)+"j"+str(j)
                add_hamiltonian_overlap_tasks(
                    self.circuit_list[i], self.circuit_list[j], self.hamiltonian, self.task_manager,task_series_id,sparse_circuit=self.sparse_circuit)
        
        self.task_manager.flush()

        coeff_list=[]

        for string_pauli in self.hamiltonian.terms:
            coeff_list.append(self.hamiltonian.terms[string_pauli])

        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                task_series_id=str(id(self)%10000)+"i"+str(i)+"j"+str(j)
                res=self.task_manager.receive_task_result(task_series_id=task_series_id)
                h=0
                for k in range(len(coeff_list)):
                    h+=res[k]*coeff_list[k]

                self.H_mat[i][j] = h
                self.H_mat[j][i] = np.conjugate(h)

                if self.progress_bar:
                    pbar.update(1)
        if self.progress_bar:
            pbar.close()
        return

    def calc_S_mat(self):
        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                if i == j:
                    self.S_mat[i][j] = 1.0
                    continue
                s = get_inner_two_circuit_product(
                    self.circuit_list[i], self.circuit_list[j])
                # print(i,j,s)
                self.S_mat[i][j] = s
                self.S_mat[j][i] = np.conjugate(s)
        return


def get_hamiltonian_overlap_0(first_circuit: BlockCircuit, second_circuit: BlockCircuit, hamiltonian):
    temp_circuit = first_circuit.duplicate()
    overlap = 0
    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            temp_circuit.add_block(PauliGatesBlock(string_pauli))
            overlap += pauli_and_coff.terms[string_pauli] * \
                get_inner_two_circuit_product(temp_circuit, second_circuit)
            temp_circuit.block_list.pop(len(temp_circuit.block_list)-1)
    return overlap


def add_hamiltonian_overlap_tasks(first_circuit: BlockCircuit, second_circuit: BlockCircuit, hamiltonian, task_manager: TaskManager, task_series_id ,sparse_circuit=False):
    for string_pauli in hamiltonian.terms:
            temp_circuit = first_circuit.duplicate()
            temp_circuit.add_block(PauliGatesBlock(string_pauli))
            task = InnerProductTask(
                temp_circuit, second_circuit, is_sparse=sparse_circuit)
            task_manager.add_task_to_buffer(
                task, task_series_id=task_series_id)


def get_growing_circuit_list(circuit: BlockCircuit):
    new_circuit = circuit.duplicate()
    circuits = [new_circuit]
    n_blocks = len(new_circuit.block_list)
    for i in range(n_blocks):
        new_circuit = new_circuit.duplicate()
        new_circuit.block_list.pop(n_blocks-1-i)
        circuits.append(new_circuit)
    return circuits
