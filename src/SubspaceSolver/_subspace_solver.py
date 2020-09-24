from Blocks import BlockCircuit
import numpy as np
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._pauli_gates_block import PauliGatesBlock
from scipy.linalg import eigh
from ParallelTaskRunner import TaskManager
from ParallelTaskRunner._mat_term_task import MatrixTermTask
from tqdm import tqdm
from Utilities.Iterators import iter_partial_operators
import time

class SubspaceSolver:
    """
    The class for Quantum Subspace Diagonalization(QSD) method,
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
        self.S_mat = np.array([[0.0] * self.n_basis] * self.n_basis, dtype=complex)
        self.H_mat = np.array([[0.0] * self.n_basis] * self.n_basis, dtype=complex)
        self.hamiltonian = hamiltonian
        self.eigvals = None
        self.eigvecs = None
        self.ground_energy = None
        self.ground_state = None

        n_qubit = circuit_list[0].n_qubit
        n_complete_basis = 2 ** n_qubit
        print(self.n_basis, "states used to construct the subspace, where the complete space is " +
              str(n_complete_basis) + "-dimensional.")

        return

    def execute(self):
        print("QSD solver Started")
        print("Calculating S matrix")
        self.calc_S_mat()
        revise_little_negative(self.S_mat)
        print("Calculating H matrix")
        self.calc_H_mat()
        
        # print(self.H_mat)
        # print(self.S_mat)
        self.eigvals, self.eigvecs = eigh(
            self.H_mat, self.S_mat, eigvals_only=False)
        self.ground_energy = self.eigvals[0]
        self.ground_state = self.eigvecs[:, 0]
        print("The ground state energy is", self.ground_energy)
        print("It's eigenvector is", self.ground_state)

    def calc_S_mat(self):
        if self.task_manager != None:
            self.S_mat=self._calc_mat_term_parellel(None)
        else:
            self._calc_S_mat_0()

    def calc_H_mat(self):
        if self.task_manager != None:
            self.H_mat=self._calc_mat_term_parellel(self.hamiltonian)
        else:
            self._calc_H_mat_0()

    def _calc_H_mat_0(self):

        if self.progress_bar:
            pbar = tqdm(total=(self.n_basis + 1) * self.n_basis // 2)
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

    def _calc_mat_term_parellel(self,hamiltonian):
        if self.progress_bar:
            pbar = tqdm(total=(self.n_basis + 1) * self.n_basis // 2)
            if hamiltonian is not None:
                pbar.set_description(str("H matrix"))
            else:
                pbar.set_description(str("S matrix"))

        task_series_id ="QSD mat"+str(time.time()%10000)
        
        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                self.task_manager.add_task_to_buffer(MatrixTermTask(self.circuit_list[i],self.circuit_list[j],hamiltonian),task_series_id=task_series_id)

        self.task_manager.flush()
        res_list = self.task_manager.receive_task_result(
                    task_series_id=task_series_id)
        res_index=0
        mat = np.array([[0.0] * self.n_basis] * self.n_basis, dtype=complex)

        for i in range(self.n_basis):
            for j in range(i, self.n_basis):
                mat[i][j] = res_list[res_index]
                mat[j][i] = np.conjugate(res_list[res_index])
                if self.progress_bar:
                    pbar.update(1)
                res_index+=1
        if self.progress_bar:
            pbar.close()
        return mat

    def _calc_S_mat_0(self):
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


VERY_SMALL_NUMBER = 1e-8


def revise_little_negative(S_mat: np.array):
    eigv = np.linalg.eigvalsh(S_mat)
    print(eigv)
    assert eigv[0] > -VERY_SMALL_NUMBER
    if eigv[0] < VERY_SMALL_NUMBER:
        S_mat += np.eye(len(S_mat)) * VERY_SMALL_NUMBER


def add_hamiltonian_overlap_tasks(first_circuit: BlockCircuit, second_circuit: BlockCircuit, hamiltonian,
                                  task_manager: TaskManager, task_series_id, sparse_circuit=False):
    for operator in iter_partial_operators(hamiltonian, task_manager.task_package_size):
        task = MatrixTermTask(first_circuit, second_circuit,
                              operator, is_sparse=sparse_circuit)
        task_manager.add_task_to_buffer(task, task_series_id=task_series_id)


def get_hamiltonian_overlap_0(first_circuit: BlockCircuit, second_circuit: BlockCircuit, hamiltonian):
    temp_circuit = first_circuit.duplicate()
    overlap = 0
    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            temp_circuit.add_block(PauliGatesBlock(string_pauli))
            overlap += pauli_and_coff.terms[string_pauli] * \
                       get_inner_two_circuit_product(temp_circuit, second_circuit)
            temp_circuit.block_list.pop(len(temp_circuit.block_list) - 1)
    return overlap


def get_growing_circuit_list(circuit: BlockCircuit):
    new_circuit = circuit.duplicate()
    circuits = [new_circuit]
    n_blocks = len(new_circuit.block_list)
    for i in range(n_blocks):
        new_circuit = new_circuit.duplicate()
        new_circuit.block_list.pop(n_blocks - 1 - i)
        circuits.append(new_circuit)
    return circuits
