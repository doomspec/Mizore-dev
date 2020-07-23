from openfermion.hamiltonians import MolecularData
from openfermion.transforms import bravyi_kitaev, get_fermion_operator
from openfermion.ops import QubitOperator
from openfermionpyscf import run_pyscf
from .Molecule._geometry_generator import geometry_generator_dict, equilibrium_geometry_dict
from .Molecule._generate_HF_operation import get_dressed_operator, get_HF_operator, get_electron_fermion_operator
from Objective._hamiltonian_obj import HamiltonianObjective
from Blocks import HartreeFockInitBlock
from Utilities.Tools import get_operator_chain

NOT_DEFINED = 999999
CHEMICAL_ACCURACY = 0.001


def get_example_molecular_hamiltonian(molecule_name, geometry_info=NOT_DEFINED, fermi_qubit_transform=bravyi_kitaev):
    if geometry_info == NOT_DEFINED:
        geometry_info = equilibrium_geometry_dict[molecule_name]

    # Get geometry
    if molecule_name not in geometry_generator_dict.keys():
        print("No such example molecule, using default H2 hamiltonian.")
        molecule_name = "H2"

    geometry = geometry_generator_dict[molecule_name](geometry_info)

    # Get fermion Hamiltonian
    basis = 'sto-3g'
    multiplicity = 1
    charge = 0
    molecule = MolecularData(geometry, basis, multiplicity, charge, str(
        geometry_info))
    molecule = run_pyscf(molecule, run_scf=1, run_fci=1)
    molecule.load()
    fermion_hamiltonian = get_fermion_operator(molecule.get_molecular_hamiltonian())

    # Map ferimon Hamiltonian to qubit Hamiltonian
    qubit_hamiltonian = fermi_qubit_transform(fermion_hamiltonian)

    # Dress the Hamiltonian so that |00..00> is the HF state

    # qubit_electron_operator=fermi_qubit_transform(get_electron_fermion_operator(molecule.n_electrons))
    qubit_electron_operator = get_HF_operator(molecule.n_electrons, fermi_qubit_transform)
    # qubit_hamiltonian=get_dressed_operator(qubit_electron_operator,qubit_hamiltonian)

    # Ignore terms in Hamiltonian that close to zero
    qubit_hamiltonian.compress()

    # Set the terminate_energy to be achieving the chemical accuracy
    terminate_energy = molecule.fci_energy + CHEMICAL_ACCURACY
    hamiltonian_info = {"n_qubit": molecule.n_qubits, "start_energy": molecule.hf_energy,
                        "terminate_energy": terminate_energy}

    init_operator = HartreeFockInitBlock(get_operator_chain(qubit_electron_operator))

    return HamiltonianObjective(qubit_hamiltonian, molecule.n_qubits, init_operator, hamiltonian_info)


def _get_example_qaoa_hamiltonian(problem, n_qubit):
    # print('r = {} A'.format(bond_len))
    if problem == 'maxcut':
        qubit_hamiltonian = get_maxcut(n_qubit)
    elif problem == 'tsp':
        qubit_hamiltonian = get_tsp(n_qubit)
    else:
        print(
            "Such example qaoa problem is not supported, using default maxcut hamiltonian.")
        qubit_hamiltonian = get_maxcut(n_qubit)

    return qubit_hamiltonian


def get_maxcut(n_qubit):
    '''
    Same with n qubit Ising model, qubit is site number.
    '''
    hamiltonian = 0 * QubitOperator("")
    coeff = 1
    for i in range(n_qubit):
        for j in range(i):
            hamiltonian += coeff * QubitOperator("Z" + str(i) + " Z" + str(j))
    hamiltonian_info = {"n_qubit": n_qubit}
    return HamiltonianObjective(hamiltonian, n_qubit, None, hamiltonian_info)


def get_tsp(n_qubit):
    # Here qubit means number of cities
    hamiltonian = 0 * QubitOperator("")
    coeff = 1 / 4
    for s in range(n_qubit):
        for i in range(n_qubit):
            hamiltonian += -coeff * QubitOperator("Z" + str(i * n_qubit + s))
            for j in range(n_qubit):
                hamiltonian += -coeff * QubitOperator("Z" + str(j * n_qubit + s + 1))
                hamiltonian += coeff * \
                               QubitOperator("Z" + str(i * n_qubit + s) + "Z" + str(j * n_qubit + s + 1))
    hamiltonian_info = {"n_qubit": n_qubit}
    return HamiltonianObjective(hamiltonian, n_qubit, None, hamiltonian_info)
