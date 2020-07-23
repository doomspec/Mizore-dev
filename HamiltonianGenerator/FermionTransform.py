from openfermion.transforms import bravyi_kitaev
from openfermion.transforms import jordan_wigner
from openfermion.transforms import binary_code_transform, parity_code


def get_parity_transformation(n_modes):
    def parity_transformation(FermionOperator):
        binary_code_transform(FermionOperator, parity_code(n_modes))

    return parity_transformation
