from ._block import Block
from Utilities.Operations import apply_Pauli_gates


class PauliGatesBlock(Block):


    n_parameter = 0
    IS_INVERSE_DEFINED = True
    IS_LOCALIZE_AVAILABLE = True


    def __init__(self, paulistring):
        """
        paulistring should be like [(0,'X'),(2,'Y')]
        """
        self.paulistring = paulistring
        """
        qsubset=[]
        for index,_pauli in paulistring:
            qsubset.append(index)
        """
        Block.__init__(self, n_parameter=0)

    def get_localized_operator(self,_qsubset):
        qsubset=set(_qsubset)
        new_paulistring=[]
        for term in self.paulistring:
            if term[0] in qsubset:
                new_paulistring.append(term)
        return PauliGatesBlock(new_paulistring)

    def apply_forward_gate(self, parameter, wavefunction):
        apply_Pauli_gates(self.paulistring, wavefunction)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        apply_Pauli_gates(self.paulistring, wavefunction)
        return

    def get_gate_used(self):
        return {"SingleRotation":len(self.paulistring)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; PauliString:" + str(self.paulistring)
        return info
