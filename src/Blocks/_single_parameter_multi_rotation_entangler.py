from ._block import Block
from Utilities.Operations import generalized_rotation
from Utilities.Tools import pauliword2string
from openfermion.ops import QubitOperator
from Utilities.Iterators import iter_coeff_qsubset_pauli_of_operator

class SingleParameterMultiRotationEntangler(Block):
    """Entangler of the form: e^{i P_1 a_1 t} e^{iP_2 a_2 t} .. e^{iP_n a_n t}
    There is only one adjustable parameter
    Attributes:
        operator: Ops = sum_i a_i P_i
    """
    IS_INVERSE_DEFINED = True

    def __init__(self, operator:QubitOperator, init_angle=None):
        Block.__init__(self,n_parameter=1)

        self.qsubset_pauliword_list=[]
        self.coeff_list=[]
        for coeff,qsubset,pauli in iter_coeff_qsubset_pauli_of_operator(operator):
            self.qsubset_pauliword_list.append((qsubset,pauli))
            self.coeff_list.append(abs(coeff)) # TODO

        if init_angle==None:
            init_angle=[0.0]
        self.parameter=init_angle
        
    def apply_forward_gate(self, parameter, wavefunction):
        for i in range(len(self.qsubset_pauliword_list)):
            qsubset, pauliword = self.qsubset_pauliword_list[i]
            #print((parameter[0]+self.parameter[0])*self.coeff_list[i])
            generalized_rotation(wavefunction, qsubset,
                                pauliword, evolution_time=(parameter[0]+self.parameter[0])*self.coeff_list[i])
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        for i in reversed(range(len(self.qsubset_pauliword_list))):
            qsubset, pauliword = self.qsubset_pauliword_list[i]
            generalized_rotation(wavefunction, qsubset,
                                pauliword, evolution_time=-(parameter[0]+self.parameter[0])*self.coeff_list[i])
        return
        
    def __str__(self):
        info=self.basic_info_string()
        info+="; N Rotation:"+str(len(self.qsubset_pauliword_list))
        info+="; "+str(self.parameter)

        #info+="; Qsubset:"+str(self.qsubset)
        #info+="; Pauli:"+pauliword2string(self.pauliword)
        return info