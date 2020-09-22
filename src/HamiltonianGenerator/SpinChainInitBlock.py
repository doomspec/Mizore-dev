
from Blocks._minor_blocks import HadamardBlock,CZBlock
from Blocks import CompositiveBlock,BlockCircuit

def get_haldane_chain_s_1_init_block(n_qubit):
    qsubset = list(range(1,n_qubit-1))
    pairset=[(i,i+1) for i in range(n_qubit-1)]
    bc=BlockCircuit(n_qubit)
    bc.add_block(HadamardBlock(qsubset))
    bc.add_block(CZBlock(pairset))
    return CompositiveBlock(bc)

def get_transverse_field_init_block(n_qubit):
    from Blocks._minor_blocks import HadamardBlock
    from Blocks._pauli_gates_block import PauliGatesBlock
    bc=BlockCircuit(n_qubit)
    bc.add_block(PauliGatesBlock([(i,"X") for i in range(n_qubit)]))
    bc.add_block(HadamardBlock(list(range(n_qubit))))
    return CompositiveBlock(bc)

