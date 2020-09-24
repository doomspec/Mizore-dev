from ParallelTaskRunner._task import Task
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._sparse_circuit_utilities import get_0000_amplitude_on_sparse_circuit
from Blocks import BlockCircuit, PauliGatesBlock
from Blocks._utilities import concatenate_circuit, get_inverse_circuit, get_0000_amplitude_on_circuit,get_inner_two_circuit_product
from Blocks._utilities import get_circuit_complete_amplitudes,evaluate_off_diagonal_term_by_amps
from Utilities.Tools import qubit_operator2matrix

class MatrixTermTask(Task):

    def __init__(self, circuit1: BlockCircuit, circuit2: BlockCircuit, hamiltonian, is_sparse=False):
        Task.__init__(self)
        self.circuit1 = circuit1
        self.circuit2 = circuit2
        self.is_sparse = is_sparse
        self.hamiltonian = hamiltonian

    def run(self):
        return get_matrix_term(self.circuit1, self.circuit2, self.hamiltonian, is_sparse=self.is_sparse)

def get_matrix_term(circuit1: BlockCircuit, circuit2: BlockCircuit, hamiltonian, is_sparse=False):
    if is_sparse:
        for _i in range(10):
            print("Sparse circuit is not supported in QSD solver now. Please wait for development.")

    if hamiltonian is not None:
        circuit1_amp = get_circuit_complete_amplitudes(circuit1)
        circuit2_amp = get_circuit_complete_amplitudes(circuit2)
        hamiltonian_mat=qubit_operator2matrix(
                circuit1.n_qubit, hamiltonian)
        mat_term=evaluate_off_diagonal_term_by_amps(
                circuit1_amp, circuit2_amp, hamiltonian_mat)
    else:
        mat_term=get_inner_two_circuit_product(circuit1,circuit2)

    return mat_term


def get_matrix_term_0(circuit1: BlockCircuit, circuit2: BlockCircuit, hamiltonian, is_sparse=False):
    temp_circuit = circuit1.duplicate()
    temp_circuit.add_block(PauliGatesBlock([(0, 'X')]))
    paulistring_index = len(temp_circuit.block_list) - 1
    temp_circuit = concatenate_circuit(temp_circuit, get_inverse_circuit(circuit2))

    mat_term = 0

    if is_sparse:
        for string_pauli in hamiltonian.terms:
            temp_circuit.block_list[paulistring_index] = PauliGatesBlock(string_pauli)
            amp0000 = get_0000_amplitude_on_sparse_circuit(temp_circuit)
            mat_term += hamiltonian.terms[string_pauli] * amp0000
    else:
        for string_pauli in hamiltonian.terms:
            temp_circuit.block_list[paulistring_index] = PauliGatesBlock(string_pauli)
            amp0000 = get_0000_amplitude_on_circuit(temp_circuit)
            mat_term += hamiltonian.terms[string_pauli] * amp0000

    return mat_term
