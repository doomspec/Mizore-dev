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

def xxz_model(n_qubit,x_coupling,z_coupling,periodic=True):
    
    z_hamiltonian=QubitOperator()
    for i in range(n_qubit-1):
        z_hamiltonian+=QubitOperator("Z"+str(i))*QubitOperator("Z"+str(i+1))
    if periodic:
        z_hamiltonian+=QubitOperator("Z"+str(n_qubit-1))*QubitOperator("Z"+str(0))
    xy_hamiltonian=QubitOperator()
    for i in range(n_qubit-1):
        xy_hamiltonian+=QubitOperator("X"+str(i))*QubitOperator("X"+str(i+1))
        xy_hamiltonian+=QubitOperator("Y"+str(i))*QubitOperator("Y"+str(i+1))
    if periodic:
        xy_hamiltonian+=QubitOperator("X"+str(n_qubit-1))*QubitOperator("X"+str(0))
        xy_hamiltonian+=QubitOperator("Y"+str(n_qubit-1))*QubitOperator("Y"+str(0))
    hamiltonian=z_coupling*z_hamiltonian+x_coupling*xy_hamiltonian
    init_list=[2*i for i in range(n_qubit//2)]
    energy_obj=EnergyObjective(hamiltonian,n_qubit,init_block=HartreeFockInitBlock(init_list))
    return energy_obj

    
if __name__ == "__main__":
    print(xxz_model(10,1,1))