from PoolGenerator import BlockPool
from openfermion.ops import FermionOperator, QubitOperator
from openfermion.transforms import bravyi_kitaev
from Blocks import MultiRotationEntangler, SingleParameterMultiRotationEntangler, BlockCircuit, CompositiveBlock
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

    from Utilities.Iterators import iter_terms_in_fermion_operator

    pool = BlockPool()
    for term in general_single_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += SingleParameterMultiRotationEntangler(qubit_excitation_operator)

    for term in uccgsd_double_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += SingleParameterMultiRotationEntangler(qubit_excitation_operator)

    return pool


def fermion_SD_excitation_multi_parameter_pool(n_qubit, fermi_qubit_transform=bravyi_kitaev):
    """
    A modified version of the pool proposed in Nat Commun 10, 3007 (2019), 
    where the parameter of every high-dimensional rotation in the ansatz is adjustable.
    """

    from Utilities.Iterators import iter_terms_in_fermion_operator

    pool = BlockPool()
    for term in general_single_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += MultiRotationEntangler(qubit_excitation_operator)

    for term in uccgsd_double_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += MultiRotationEntangler(qubit_excitation_operator)

    return pool


def upccgsd_pool(n_qubit, fermi_qubit_transform=bravyi_kitaev):
    """Pools proposed in J. Chem. Theory Comput. 2018, 15, 311–324., also called k-UpCCGSD.
    Operators are single and pair double unitary excitation operators.
    Args:
        n_qubit: number of qubits to generate excitation operators
        fermi_qubit_transform: transformation, default bravyi_kitaev
    Return:
        Class MultiRotationEntangler with attribute QubitOperator
    """

    pool = BlockPool()
    for term in general_single_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += SingleParameterMultiRotationEntangler(qubit_excitation_operator)

    for term in upccgsd_double_generator(n_qubit):
        qubit_excitation_operator = fermi_qubit_transform(term)
        pool += SingleParameterMultiRotationEntangler(qubit_excitation_operator)

    return pool


def get_general_single_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    n_parameters = 2 * n_single_amplitudes
    return n_parameters


def get_uccgsd_double_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    n_parameters = n_single_amplitudes * n_single_amplitudes
    return n_parameters


def get_upccgsd_double_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    n_parameters = n_single_amplitudes
    return n_parameters


def general_single_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    amplitude = 1.0

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    for spin in range(2):
        for i in range(n_spatial_orbitals):
            for a in range(i + 1, n_spatial_orbitals):
                # Generate single excitations
                coeff = amplitude
                generator += FermionOperator((
                    (2 * a + spin, 1),
                    (2 * i + spin, 0)),
                    coeff)
                if anti_hermitian:
                    generator += FermionOperator((
                        (2 * i + spin, 1),
                        (2 * a + spin, 0)),
                        -coeff)

                yield generator


def uccgsd_double_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    amplitude = 1.0
    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate double excitations
            for j in range(n_spatial_orbitals):
                for b in range(j + 1, n_spatial_orbitals):
                    coeff = amplitude
                    generator += FermionOperator((
                        (2 * a, 1),
                        (2 * i, 0),
                        (2 * b + 1, 1),
                        (2 * j + 1, 0)),
                        coeff)
                    if anti_hermitian:
                        generator += FermionOperator((
                            (2 * i, 1),
                            (2 * a, 0),
                            (2 * j + 1, 1),
                            (2 * b + 1, 0)),
                            -coeff)

                    yield generator


def upccgsd_double_generator(n_qubit, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    amplitude = 1.0

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate double excitations
            coeff = amplitude
            generator += FermionOperator((
                (2 * a, 1),
                (2 * i, 0),
                (2 * a + 1, 1),
                (2 * i + 1, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2 * i, 1),
                    (2 * a, 0),
                    (2 * i + 1, 1),
                    (2 * a + 1, 0)),
                    -coeff)

            yield generator
