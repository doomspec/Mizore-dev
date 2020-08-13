from projectq.ops import H, X, All, Measure, CNOT, Z, Rz, Ry, Rx, C
import math


def apply_X_gates(qsubset, wavefunction):
    for i in qsubset:
        X | wavefunction[i]


def CNOT_entangler(wavefunction, qsubset):
    for i in range(len(qsubset)-1):
        CNOT | (wavefunction[qsubset[i]], wavefunction[qsubset[i+1]])
    CNOT | (wavefunction[qsubset[i+1]], wavefunction[qsubset[0]])


def inversed_CNOT_entangler(wavefunction, qsubset):

    CNOT | (wavefunction[qsubset[len(qsubset)-1]], wavefunction[qsubset[0]])
    for i in reversed(range(len(qsubset)-1)):
        CNOT | (wavefunction[qsubset[i]], wavefunction[qsubset[i+1]])


def XY_full_rotation(wavefunction, qsubset, parameter):
    """
    Apply Rx(t1)Ry(t2) rotation to all the qubits with different angle
    """
    n_qubit = len(qsubset)
    for i in range(len(qsubset)):
        Rx(parameter[i]) | wavefunction[qsubset[i]]
        Ry(parameter[n_qubit+i]) | wavefunction[qsubset[i]]


def inversed_XY_full_rotation(wavefunction, qsubset, parameter):
    """
    The inversed operation of XY_full_rotation() of the same parameter
    """
    n_qubit = len(qsubset)
    for i in range(len(qsubset)):
        Ry(-parameter[n_qubit+i]) | wavefunction[qsubset[i]]
        Rx(-parameter[i]) | wavefunction[qsubset[i]]


def full_rotation(wavefunction, qsubset, parameter):
    """
    Apply Rx(t1)Ry(t2)Rx(t3) rotation to all the qubits with different angle
    """
    n_qubit = len(qsubset)
    for i in range(len(qsubset)):
        Rx(parameter[i]) | wavefunction[qsubset[i]]
        Rz(parameter[n_qubit+i]) | wavefunction[qsubset[i]]
        Rx(parameter[2*n_qubit+i]) | wavefunction[qsubset[i]]


def inversed_full_rotation(wavefunction, qsubset, parameter):
    """
    The inversed operation of full_rotation() of the same parameter
    """
    n_qubit = len(qsubset)
    for i in range(len(qsubset)):
        Rx(-parameter[2*n_qubit+i]) | wavefunction[qsubset[i]]
        Rz(-parameter[n_qubit+i]) | wavefunction[qsubset[i]]
        Rx(-parameter[i]) | wavefunction[qsubset[i]]


def generalized_rotation(wavefunction, qsubset, pauliword, evolution_time):
    """Apply e^{iPt} on the wavefunction
    Args:
        qsubset: The subset of qubits in the wavefunction that the operation applies on
        pauliword: The Pauli word P in e^{iPt}
        evolution_time: t in e^{iPt}
    """
    HALF_PI = math.pi / 2
    n_qubit = len(qsubset)

    # Exponentiating each Pauli string requires five parts

    # 1. Perform basis rotations
    for p in range(0, n_qubit):
        pop = pauliword[p]  # Pauli op
        if pop == 1:
            H | wavefunction[qsubset[p]]  # Hadamard
        elif pop == 2:
            Rx(HALF_PI) | wavefunction[qsubset[p]]

    # 2. First set CNOTs
    prev_index = None

    for p in range(0, n_qubit):
        pop = pauliword[p]  # Pauli op
        if pop == 0:
            continue
        if prev_index is not None:
            CNOT | (wavefunction[prev_index], wavefunction[qsubset[p]])
        prev_index = qsubset[p]

    # 3. Rotation (Note kexp & Ntrot)
    Rz(evolution_time * 2) | wavefunction[prev_index]

    # 4. Second set of CNOTs
    prev_index = None
    for p in reversed(range(0, n_qubit)):
        pop = pauliword[p]  # Pauli op
        if pop == 0:
            continue
        if prev_index is not None:
            CNOT | (wavefunction[qsubset[p]], wavefunction[prev_index])
        prev_index = qsubset[p]

    # 5. Rotate back to Z basis
    for p in range(0, len(pauliword)):
        pop = pauliword[p]  # Pauli op
        if pop == 1:
            H | wavefunction[qsubset[p]]  # Hadamard
        elif pop == 2:
            Rx(-HALF_PI) | wavefunction[qsubset[p]]
