from PoolGenerator import BlockPool
from openfermion.ops import FermionOperator, QubitOperator
from openfermion.transforms import bravyi_kitaev
from Blocks import MultiRotationEntangler,SingleParameterMultiRotationEntangler,BlockCircuit,CompositiveBlock
from copy import copy

def fermion_SD_excitation_single_parameter_pool(n_qubit, fermi_qubit_transform=bravyi_kitaev):
    """
    Pools proposed in Nat Commun 10, 3007 (2019), also called ADAPT-VQE.
    Operators are single and double unitary excitation operators
    Args:
        n_qubit: number of qubits to generate excitation operators
    Yield:
        SingleParameterMultiRotationEntangler
    """
    
    excitation_operators = general_single_generator(n_qubit)+uccgsd_double_generator(n_qubit)

    from Utilities.Iterators import iter_terms_in_fermion_operator
    
    for term in iter_terms_in_fermion_operator(excitation_operators):
        qubit_excitation_operator=fermi_qubit_transform(excitation_operators)
        yield SingleParameterMultiRotationEntangler(qubit_excitation_operator)

def fermion_SD_excitation_multi_parameter_pool(n_qubit, fermi_qubit_transform=bravyi_kitaev):
    """
    A modified version of the pool proposed in Nat Commun 10, 3007 (2019), 
    where the parameter of every high-dimensional rotation in the ansatz is adjustable.
    """
    excitation_operators = general_single_generator(n_qubit)+uccgsd_double_generator(n_qubit)

    from Utilities.Iterators import iter_terms_in_fermion_operator
    
    for term in iter_terms_in_fermion_operator(excitation_operators):
        qubit_excitation_operator=fermi_qubit_transform(excitation_operators)
        yield MultiRotationEntangler(qubit_excitation_operator)


def upccgsd_pool(n_qubit, fermi_qubit_transform=bravyi_kitaev):
    """Pools proposed in J. Chem. Theory Comput. 2018, 15, 311–324., also called k-UpCCGSD.
    Operators are single and pair double unitary excitation operators.
    Args:
        n_qubit: number of qubits to generate excitation operators
        fermi_qubit_transform: transformation, default bravyi_kitaev
    Return:
        Class MultiRotationEntangler with attribute QubitOperator
    """
    
    excitation_operators = general_single_generator(n_qubit)+upccgsd_double_generator(n_qubit)
    from Utilities.Iterators import iter_terms_in_fermion_operator
    circuit=BlockCircuit(n_qubit)
    for term in iter_terms_in_fermion_operator(excitation_operators):
        qubit_excitation_operator=fermi_qubit_transform(excitation_operators)
        circuit.add_block(SingleParameterMultiRotationEntangler(qubit_excitation_operator))
    yield CompositiveBlock(circuit)

def get_general_single_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals-1) // 2
    n_parameters = 2*n_single_amplitudes
    return n_parameters

def get_uccgsd_double_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals-1) // 2
    n_parameters = n_single_amplitudes*n_single_amplitudes
    return n_parameters

def get_upccgsd_double_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals-1) // 2
    n_parameters = n_single_amplitudes
    return n_parameters

def general_single_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    # Unpack amplitudes
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals-1) // 2
    n_parameters = get_general_single_parameter_number(n_qubit)
    packed_amplitudes = [1]*n_parameters
    # Single amplitudes
    t1_1 = packed_amplitudes[:n_single_amplitudes]
    t1_2 = packed_amplitudes[n_single_amplitudes:2*n_single_amplitudes]

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    count = 0
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate single excitations
            coeff = t1_1[count]
            generator += FermionOperator((
                (2*a, 1),
                (2*i, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2*i, 1),
                    (2*a, 0)),
                    -coeff)

            coeff = t1_2[count]
            generator += FermionOperator((
                (2*a+1, 1),
                (2*i+1, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2*i+1, 1),
                    (2*a+1, 0)),
                    -coeff)

            count += 1

    return generator

def uccgsd_double_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    # Unpack amplitudes
    n_parameters = get_uccgsd_double_parameter_number(n_qubit)
    packed_amplitudes = [1]*n_parameters

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    count_d = 0
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate double excitations
            for j in range(n_spatial_orbitals):
                for b in range(j + 1, n_spatial_orbitals):
                    coeff = packed_amplitudes[count_d]
                    generator += FermionOperator((
                        (2*a, 1),
                        (2*i, 0),
                        (2*b+1, 1),
                        (2*j+1, 0)),
                        coeff)
                    if anti_hermitian:
                        generator += FermionOperator((
                            (2*i, 1),
                            (2*a, 0),
                            (2*j+1, 1),
                            (2*b+1, 0)),
                            -coeff)

                    count_d += 1

    return generator

def upccgsd_double_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    # Unpack amplitudes
    n_parameters = get_upccgsd_double_parameter_number(n_qubit)
    packed_amplitudes = [1]*n_parameters

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    count_d = 0
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate double excitations
            coeff = packed_amplitudes[count_d]
            generator += FermionOperator((
                (2*a, 1),
                (2*i, 0),
                (2*a+1, 1),
                (2*i+1, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2*i, 1),
                    (2*a, 0),
                    (2*i+1, 1),
                    (2*a+1, 0)),
                    -coeff)
        
            count_d += 1

    return generator
