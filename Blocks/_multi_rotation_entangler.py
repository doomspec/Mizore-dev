from Blocks import Block
from Utilities.Operations import generalized_rotation
from Utilities.Tools import pauliword2string
from openfermion.ops import QubitOperator
from Utilities.Iterators import iter_qsubset_pauli_of_operator


class MultiRotationEntangler(Block):
    """Entangler of the form: e^{iP_1 t_1} e^{iP_2 t_1} .. e^{iP_n t_n}
    Attributes:
        operator: Ops = sum_i a_i P_i
    """
    IS_INVERSE_DEFINED = True

    def __init__(self, operator: QubitOperator, init_angle=None):
        Block.__init__(self)
        self.qsubset_pauliword_list = []
        n_parameter = 0
        for qsubset, pauli in iter_qsubset_pauli_of_operator(operator):
            n_parameter += 1
            self.qsubset_pauliword_list.append((qsubset, pauli))
        if init_angle == None:
            init_angle = [0.0] * n_parameter
        self.n_parameter = n_parameter
        self.parameter = init_angle

    def apply_forward_gate(self, parameter, wavefunction):
        for i in range(len(self.qsubset_pauliword_list)):
            qsubset, pauliword = self.qsubset_pauliword_list[i]
            generalized_rotation(wavefunction, qsubset,
                                 pauliword, evolution_time=parameter[i] + self.parameter[i])
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        for i in reversed(range(len(self.qsubset_pauliword_list))):
            qsubset, pauliword = self.qsubset_pauliword_list[i]
            generalized_rotation(wavefunction, qsubset,
                                 pauliword, evolution_time=-(parameter[i] + self.parameter[i]))
        return

    def __str__(self):
        info = self.basic_info_string()
        info += "; N Rotation:" + str(len(self.qsubset_pauliword_list))
        info += "; " + str(self.parameter)

        # info+="; Qsubset:"+str(self.qsubset)
        # info+="; Pauli:"+pauliword2string(self.pauliword)
        return info
