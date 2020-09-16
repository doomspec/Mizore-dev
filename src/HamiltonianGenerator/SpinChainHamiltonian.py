from openfermion.ops import QubitOperator
from Objective import EnergyObjective
from Blocks import HartreeFockInitBlock

def transverse_field_ising(n_qubit,field,spin_coupling=1,periodic=True):

    spin_coupling_hamiltonian=QubitOperator()
    for i in range(n_qubit-1):
        spin_coupling_hamiltonian+=QubitOperator("Z"+str(i))*QubitOperator("Z"+str(i+1))
    if periodic:
        spin_coupling_hamiltonian+=QubitOperator("Z"+str(n_qubit-1))*QubitOperator("Z"+str(0))
    field_hamitonian=QubitOperator()
    for i in range(n_qubit):
        field_hamitonian+=QubitOperator("X"+str(i))
    hamiltonian=spin_coupling*spin_coupling_hamiltonian+field*field_hamitonian
    init_list=[2*i for i in range(n_qubit//2)]
    energy_obj=EnergyObjective(hamiltonian,n_qubit,init_block=HartreeFockInitBlock(init_list))
    return energy_obj

def xxz_model(n_qubit,z_coupling,x_coupling=1,periodic=True):
    
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


def haldane_chain_s_1(n_qubit,h1,h2,J=1):
    part1=QubitOperator()
    for i in range(n_qubit-2):
        part1+=QubitOperator("Z"+str(i)+" X"+str(i+1)+" Z"+str(i+2))
    part2=QubitOperator()
    for i in range(n_qubit):
        part2+=QubitOperator("X"+str(i))
    part3=QubitOperator()
    for i in range(n_qubit-1):
        part3+=QubitOperator("X"+str(i)+" X"+str(i+1))
    hamiltonian=-J*part1-h1*part2-h2*part3
    from .SpinChainInitBlock import AD_HOC_haldane_chain_s_1_InitBlock
    energy_obj=EnergyObjective(hamiltonian,n_qubit,init_block=AD_HOC_haldane_chain_s_1_InitBlock(n_qubit))
    return energy_obj

# DQCP see arXiv:1904.00010 "Deconfined quantum critical point in one dimension"
def DQCP_chain(n_qubit,jx,jz,k2x,k2z,periodic=True):
    hamiltonian=QubitOperator()
    for i in range(n_qubit-1):
        hamiltonian+=(-jx)*QubitOperator("X"+str(i)+" X"+str(i+1))
        hamiltonian+=(-jz)*QubitOperator("Z"+str(i)+" Z"+str(i+1))
    if periodic:
        hamiltonian+=(-jx)*QubitOperator("X"+str(n_qubit-1)+" X"+str(0))
        hamiltonian+=(-jz)*QubitOperator("Z"+str(n_qubit-1)+" Z"+str(0))
    for i in range(n_qubit-2):
        hamiltonian+=k2x*QubitOperator("X"+str(i)+" X"+str(i+2))
        hamiltonian+=k2z*QubitOperator("Z"+str(i)+" Z"+str(i+2))
    if periodic:
        hamiltonian+=k2x*QubitOperator("X"+str(n_qubit-2)+" X"+str(0))
        hamiltonian+=k2z*QubitOperator("Z"+str(n_qubit-2)+" Z"+str(0))
        hamiltonian+=k2x*QubitOperator("X"+str(n_qubit-1)+" X"+str(1))
        hamiltonian+=k2z*QubitOperator("Z"+str(n_qubit-1)+" Z"+str(1))
    return EnergyObjective(hamiltonian,n_qubit)


def DQCP_chain_reparameterized(n_qubit,delta,k2,periodic=True):
    jx=1-delta
    jz=1+delta
    k2x=k2
    k2z=k2
    return DQCP_chain(n_qubit,jx,jz,k2x,k2z,periodic=periodic)
