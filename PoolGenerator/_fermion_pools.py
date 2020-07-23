from PoolGenerator import BlockPool
from openfermion.ops import FermionOperator, QubitOperator
from openfermion.transforms import bravyi_kitaev
from Blocks._multi_rotation_entangler import MultiRotationEntangler
from copy import copy


def fermion_pool(n_qubit, packed_amplitudes=None, hamiltonian=QubitOperator(()), fermi_qubit_transform=bravyi_kitaev):
    """Pools proposed in Nat Commun 10, 3007 (2019), also called ADAPT-VQE.
    Operators are single and double unitary excitation operators
    Args:
        n_qubit: number of qubits to generate excitation operators
        packed_amplitudes: variational parameters, defaul all 0
        hamiltonian: if or not only choose excitations from hamiltonian
        fermi_qubit_transform: transformation, default bravyi_kitaev
    Return:
        Class MultiRotationEntangler with attribute QubitOperator
    """
    n_parameters = get_uccgsd_parameter_number(n_qubit)
    if packed_amplitudes == None:
        packed_amplitudes = [0.0] * n_parameters

    if hamiltonian == QubitOperator(()):
        hamiltonian = fermi_qubit_transform(uccgsd_generator(n_qubit, packed_amplitudes))
    return MultiRotationEntangler(hamiltonian)


def get_uccgsd_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    n_parameters = 2 * n_single_amplitudes + n_single_amplitudes * n_single_amplitudes
    return n_parameters


def uccgsd_generator(n_qubit, packed_amplitudes, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    # Unpack amplitudes
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    # Single amplitudes
    t1_1 = packed_amplitudes[:n_single_amplitudes]
    t1_2 = packed_amplitudes[n_single_amplitudes:2 * n_single_amplitudes]
    # Double amplitudes associated with one pair
    t2_1 = packed_amplitudes[2 * n_single_amplitudes:]

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    count = 0
    count_d = 0
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate single excitations
            coeff = t1_1[count]
            generator += FermionOperator((
                (2 * a, 1),
                (2 * i, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2 * i, 1),
                    (2 * a, 0)),
                    -coeff)

            coeff = t1_2[count]
            generator += FermionOperator((
                (2 * a + 1, 1),
                (2 * i + 1, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2 * i + 1, 1),
                    (2 * a + 1, 0)),
                    -coeff)

            # Generate double excitations
            for j in range(n_spatial_orbitals):
                for b in range(j + 1, n_spatial_orbitals):
                    coeff = t2_1[count_d]
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

                    count_d += 1

            count += 1

    return generator


def upccgsd_pool(n_qubit, packed_amplitudes=None, fermi_qubit_transform=bravyi_kitaev):
    """Pools proposed in J. Chem. Theory Comput. 2018, 15, 311–324., also called k-UpCCGSD.
    Operators are single and pair double unitary excitation operators.
    Args:
        n_qubit: number of qubits to generate excitation operators
        packed_amplitudes: variational parameters, defaul all 0
        fermi_qubit_transform: transformation, default bravyi_kitaev
    Return:
        Class MultiRotationEntangler with attribute QubitOperator
    """
    n_parameters = get_upccgsd_parameter_number(n_qubit)
    if packed_amplitudes == None:
        packed_amplitudes = [0.0] * n_parameters

    hamiltonian = fermi_qubit_transform(upccgsd_generator(n_qubit, packed_amplitudes))

    return MultiRotationEntangler(hamiltonian)


def get_upccgsd_parameter_number(n_qubit):
    n_spatial_orbitals = n_qubit // 2
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2
    n_parameters = 3 * n_single_amplitudes
    return n_parameters


def upccgsd_generator(n_qubit, packed_amplitudes, anti_hermitian=True):
    if n_qubit % 2 != 0:
        raise ValueError('The total number of spin-orbitals should be even.')

    n_spatial_orbitals = n_qubit // 2
    # Unpack amplitudes
    n_single_amplitudes = n_spatial_orbitals * (n_spatial_orbitals - 1) // 2

    # Single amplitudes
    t1_1 = packed_amplitudes[:n_single_amplitudes]
    t1_2 = packed_amplitudes[n_single_amplitudes:2 * n_single_amplitudes]
    # Double amplitudes with a pair
    t2_1 = packed_amplitudes[2 * n_single_amplitudes:]

    # Initialize operator
    generator = FermionOperator()

    # Generate excitations
    count = 0
    for i in range(n_spatial_orbitals):
        for a in range(i + 1, n_spatial_orbitals):
            # Generate single excitations
            coeff = t1_1[count]
            generator += FermionOperator((
                (2 * a, 1),
                (2 * i, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2 * i, 1),
                    (2 * a, 0)),
                    -coeff)

            coeff = t1_2[count]
            generator += FermionOperator((
                (2 * a + 1, 1),
                (2 * i + 1, 0)),
                coeff)
            if anti_hermitian:
                generator += FermionOperator((
                    (2 * i + 1, 1),
                    (2 * a + 1, 0)),
                    -coeff)

            # Generate double excitations
            coeff = t2_1[count]
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

            count += 1

    return generator
