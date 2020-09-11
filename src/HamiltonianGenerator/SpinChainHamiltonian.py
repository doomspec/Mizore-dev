from openfermion.ops import QubitOperator
from Objective import EnergyObjective
from Blocks import HartreeFockInitBlock
def transverse_field_ising(n_qubit,spin_coupling,field,periodic=True):
    spin_coupling_hamiltonian=QubitOperator()
    for i in range(n_qubit-1):
        spin_coupling_hamiltonian+=QubitOperator("Z"+str(i))*QubitOperator("Z"+str(i+1))
    if periodic:
        spin_coupling_hamiltonian+=QubitOperator("Z"+str(n_qubit-1))*QubitOperator("Z"+str(0))
    spin_coupling_hamiltonian*=spin_coupling
    field_hamitonian=QubitOperator()
    for i in range(n_qubit):
        field_hamitonian+=QubitOperator("X"+str(i))
    field_hamitonian*=field
    hamiltonian=spin_coupling_hamiltonian+field_hamitonian
    init_list=[2*i for i in range(n_qubit//2)]
    energy_obj=EnergyObjective(hamiltonian,n_qubit,init_block=HartreeFockInitBlock(init_list))
    return energy_obj

if __name__ == "__main__":
    transverse_field_ising(10,1,1)