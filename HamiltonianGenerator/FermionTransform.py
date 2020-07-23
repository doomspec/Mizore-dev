from openfermion.transforms import bravyi_kitaev
from openfermion.transforms import jordan_wigner
from openfermion.transforms import binary_code_transform,parity_code
from openfermion.ops import FermionOperator,QubitOperator

def get_parity_transformation(n_modes):
    def parity_transformation(FermionOperator):
        binary_code_transform(FermionOperator,parity_code(n_modes))
    return parity_transformation


def make_transformation_spin_separating(transform,n_qubit):
    def new_transform(fermion_operator:FermionOperator):
        
        return
    return new_transform


def rearrange_sites(hamiltonian, change_rule):
    """
    Can only deal with fermion and qubit operator!!
    Rearrange the order of the spin orbitals
    -- change_rule: should be an array e.g. [0,3,2,1,4,5,6,7]  means exchange 3,1
    """
    new_hamiltonian = None
    is_qubit = True
    if isinstance(hamiltonian, QubitOperator):
        new_hamiltonian = QubitOperator()
        is_qubit = True
    if isinstance(hamiltonian, FermionOperator):
        new_hamiltonian = FermionOperator()
        is_qubit = False

    for pauli_and_coff in hamiltonian.get_operators():
        for string_pauli in pauli_and_coff.terms:
            # string_pauli is like ( (1, 'X'), (2, 'Y')  )
            new_str = list(string_pauli)
            for i in range(0, len(string_pauli)):
                new_str[i] = (change_rule[string_pauli[i][0]], string_pauli[i][1])

            if is_qubit:
                new_hamiltonian += pauli_and_coff.terms[string_pauli] * \
                    pauli2qubit_operator(new_str)
            else:
                new_hamiltonian += pauli_and_coff.terms[string_pauli] * \
                    arr2fermion_operator(new_str)

    if new_hamiltonian == None:
        raise Exception("Error, please check the type of the input Hamiltonian!")

    return new_hamiltonian

def separate_odd_even_map(n_spinorbitals):
    """
    Put the spin orbital of odd index to the last, making the first half spin up and follows spin down
    """
    if n_spinorbitals%2 != 0:
        print("n_spinorbitals is not even!")
        return
    rule=[0]*n_spinorbitals
    for i in range(0,n_spinorbitals):
        if i%2==0:
            rule[i]=i//2
        else:
            rule[i]=i//2+n_spinorbitals//2
    return rule

def pauli2qubit_operator(string_pauli):
    """
    string_pauli:  like( (1, 'X'), (2, 'Y')  )
    for every element k in it,k[0] is the qubit it act, k[1] is the pauli
    Return a QubitOperator without coefficient
    """
    p_str = ""
    for k in string_pauli:
        if k[1] != 'I':
            p_str = p_str+k[1]+str(k[0])+" "
    return QubitOperator(p_str)


def arr2fermion_operator(string_pauli):
    """
    string_pauli:  like( (1, 1), (2, 0)  )
    for every element k in it,k[0] is the qubit it act, k[1] is the pauli
    Return a Fermion without coefficient
    """
    p_str = ""
    for k in string_pauli:
        if k[1] == 1:
            p_str = p_str+str(k[0])+"^"+" "
        else:
            p_str = p_str+str(k[0])+" "
    return FermionOperator(p_str)