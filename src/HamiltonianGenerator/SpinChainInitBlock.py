
from Blocks import CompositiveBlock,BlockCircuit,Block
from Utilities.Operations import apply_H_gates,apply_CZ_gates

class AD_HOC_haldane_chain_s_1_InitBlock(Block):

    n_parameter = 0
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = False

    def __init__(self, n_qubit):
        Block.__init__(self, n_parameter=0)
        self.qsubset = list(range(1,n_qubit-1))
        self.pairset=[(i,i+1) for i in range(n_qubit-1)]

    def apply_forward_gate(self, parameter, wavefunction):
        apply_H_gates(self.qsubset, wavefunction)
        apply_CZ_gates(self.pairset,wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_CZ_gates(self.pairset,wavefunction)
        apply_H_gates(self.qsubset, wavefunction)
        return

    def get_gate_used(self):
        return {"SingleRotation": len(self.qsubset),"CZ":len(self.pairset)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        return info