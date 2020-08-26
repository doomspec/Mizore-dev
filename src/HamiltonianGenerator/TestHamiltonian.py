from openfermion.hamiltonians import MolecularData
from openfermion.transforms import bravyi_kitaev, get_fermion_operator
from openfermion.ops import QubitOperator
from .Molecule._mizore_run_pyscf import run_pyscf
from .Molecule._geometry_generator import geometry_generator_dict, equilibrium_geometry_dict
from .Molecule._generate_HF_operation import get_dressed_operator, get_HF_operator, get_electron_fermion_operator
from Objective._energy_obj import EnergyObjective
from Blocks import HartreeFockInitBlock
from Utilities.Tools import get_operator_chain

NOT_DEFINED = 999999
CHEMICAL_ACCURACY = 0.001

"""
The methods for generating simple molecular and graph theory Hamiltonian for VQE to find ground state energy.

make_example_H2, make_example_LiH, make_example_H2O and make_example_N2 are the main methods
Use default parameter will produce a standard Hamiltonian for benchmarking

make_molecular_energy_obj can be used to generate Hamiltonians in a more expert way
Selecting active space based on *Irrep* is implemented in Mizore based on PySCF
Please refer to the document of PySCF to see how to use the irrep symbols
"""


def make_example_H2(basis="sto-3g",
                    geometry_info=equilibrium_geometry_dict["H2"],
                    fermi_qubit_transform=bravyi_kitaev,
                    is_computed=False):
    return make_molecular_energy_obj(molecule_name="H2", basis=basis, geometry_info=geometry_info, fermi_qubit_transform=fermi_qubit_transform, is_computed=is_computed)


def make_example_LiH(basis="sto-3g",
                     geometry_info=equilibrium_geometry_dict["LiH"],
                     fermi_qubit_transform=bravyi_kitaev,
                     is_computed=False):
    n_cancel_orbital = 2
    n_frozen_orbital = 1
    cas_irrep_nocc = {'A1': 3}
    cas_irrep_ncore = {'E1x': 0,'E1y': 0}
    return make_molecular_energy_obj(molecule_name="LiH", basis=basis, geometry_info=geometry_info, n_cancel_orbital=n_cancel_orbital, n_frozen_orbital=n_frozen_orbital, cas_irrep_nocc=cas_irrep_nocc, cas_irrep_ncore=cas_irrep_ncore, fermi_qubit_transform=fermi_qubit_transform, is_computed=is_computed)


def make_example_H2O(basis="6-31g",
                     geometry_info=equilibrium_geometry_dict["H2O"],
                     fermi_qubit_transform=bravyi_kitaev,
                     is_computed=False):
    n_cancel_orbital = 5
    n_frozen_orbital = 3
    cas_irrep_nocc = {'B1': 2, 'A1': 3}
    cas_irrep_ncore = {'B1': 0, 'A1': 2}
    return make_molecular_energy_obj(molecule_name="H2O", basis=basis, geometry_info=geometry_info, n_cancel_orbital=n_cancel_orbital, n_frozen_orbital=n_frozen_orbital, cas_irrep_nocc=cas_irrep_nocc, cas_irrep_ncore=cas_irrep_ncore, fermi_qubit_transform=fermi_qubit_transform, is_computed=is_computed)


def make_example_N2(basis="cc-pvdz", geometry_info=equilibrium_geometry_dict["N2"], fermi_qubit_transform=bravyi_kitaev, is_computed=False):
    n_cancel_orbital = 18
    n_frozen_orbital = 2
    return make_molecular_energy_obj(molecule_name="N2", basis=basis, geometry_info=geometry_info, n_cancel_orbital=n_cancel_orbital, n_frozen_orbital=n_frozen_orbital, fermi_qubit_transform=fermi_qubit_transform, is_computed=is_computed)


def make_molecular_energy_obj(molecule_name, basis="sto-3g", geometry_info=None, n_cancel_orbital=0, n_frozen_orbital=0, cas_irrep_nocc=None, cas_irrep_ncore=None, fermi_qubit_transform=bravyi_kitaev, is_computed=False):

    if geometry_info == None:
        geometry_info = equilibrium_geometry_dict[molecule_name]

    # Get geometry
    if molecule_name not in geometry_generator_dict.keys():
        print("No such example molecule, using default H2 hamiltonian.")
        molecule_name = "H2"

    geometry = geometry_generator_dict[molecule_name](geometry_info)

    # Get fermion Hamiltonian

    multiplicity = 1
    charge = 0
    molecule = MolecularData(geometry, basis, multiplicity, charge, str(
        geometry_info))
    molecule.symmetry = True
    if not is_computed:
        molecule = run_pyscf(molecule, run_fci=1, n_frozen_orbital=n_frozen_orbital,
                             n_cancel_orbital=n_cancel_orbital, cas_irrep_nocc=cas_irrep_nocc, cas_irrep_ncore=cas_irrep_ncore)
    molecule.load()

    active_space_start = n_frozen_orbital
    active_space_stop = molecule.n_orbitals-n_cancel_orbital
    n_active_orb = active_space_stop-active_space_start
    molecule.n_orbitals = n_active_orb
    molecule.n_qubits = n_active_orb*2
    molecule.n_electrons = molecule.n_electrons-active_space_start*2


    fermion_hamiltonian = get_fermion_operator(
        molecule.get_molecular_hamiltonian(occupied_indices=molecule.frozen_orbitals, active_indices=molecule.active_orbitals))

    # Map ferimon Hamiltonian to qubit Hamiltonian
    qubit_hamiltonian = fermi_qubit_transform(fermion_hamiltonian)

    # qubit_electron_operator=fermi_qubit_transform(get_electron_fermion_operator(molecule.n_electrons))
    qubit_electron_operator = get_HF_operator(
        molecule.n_electrons, fermi_qubit_transform)
    # qubit_hamiltonian=get_dressed_operator(qubit_electron_operator,qubit_hamiltonian)

    # Ignore terms in Hamiltonian that close to zero
    qubit_hamiltonian.compress()

    # Set the terminate_energy to be achieving the chemical accuracy
    terminate_energy = molecule.fci_energy + CHEMICAL_ACCURACY
    obj_info = {"n_qubit": molecule.n_qubits, "start_cost": molecule.hf_energy,
                "terminate_cost": terminate_energy}

    init_operator = HartreeFockInitBlock(
        get_operator_chain(qubit_electron_operator))


    return EnergyObjective(qubit_hamiltonian, molecule.n_qubits, init_operator, obj_info)


def _get_example_qaoa_hamiltonian(problem, n_qubit):
    # print('r = {} A'.format(bond_len))
    if problem == 'maxcut':
        qubit_hamiltonian = get_maxcut_hamiltonian(n_qubit)
    elif problem == 'tsp':
        qubit_hamiltonian = get_tsp_hamiltonian(n_qubit)
    else:
        print(
            "Such example qaoa problem is not supported, using default maxcut hamiltonian.")
        qubit_hamiltonian = get_maxcut_hamiltonian(n_qubit)

    return qubit_hamiltonian


def get_maxcut_hamiltonian(n_qubit):
    '''
    Same with n qubit Ising model, qubit is site number.
    '''
    hamiltonian = 0 * QubitOperator("")
    coeff = 1
    for i in range(n_qubit):
        for j in range(i):
            hamiltonian += coeff * QubitOperator("Z" + str(i) + " Z" + str(j))
    obj_info = {"n_qubit": n_qubit}
    return EnergyObjective(hamiltonian, n_qubit, None, obj_info)


def get_tsp_hamiltonian(n_qubit):
    # Here qubit means number of cities
    hamiltonian = 0 * QubitOperator("")
    coeff = 1 / 4
    for s in range(n_qubit):
        for i in range(n_qubit):
            hamiltonian += -coeff * QubitOperator("Z" + str(i * n_qubit + s))
            for j in range(n_qubit):
                hamiltonian += -coeff * \
                    QubitOperator("Z" + str(j * n_qubit + s + 1))
                hamiltonian += coeff * \
                    QubitOperator("Z" + str(i * n_qubit + s) +
                                  "Z" + str(j * n_qubit + s + 1))
    obj_info = {"n_qubit": n_qubit}
    return EnergyObjective(hamiltonian, n_qubit, None, obj_info)
