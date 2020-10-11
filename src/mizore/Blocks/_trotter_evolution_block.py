from ._block import Block
from ..Utilities.Operations import generalized_rotation
from ..Utilities.Tools import get_operator_qsubset
from openfermion.ops import QubitOperator
from ..Utilities.Iterators import iter_coeff_qsubset_pauli_of_operator
from ._rotation_entangler import count_single_gate_for_pauliword

class TrotterTimeEvolutionBlock(Block):

    n_parameter = 1
    IS_INVERSE_DEFINED = True

    def __init__(self, hamiltonian: QubitOperator, n_trotter_step=1, evolution_time=0):
        Block.__init__(self,n_parameter = 1)
        self.n_trotter_step=n_trotter_step
        self.qsubset_pauliword_list=[]
        for term in iter_coeff_qsubset_pauli_of_operator(hamiltonian):
            self.qsubset_pauliword_list.append(term)
            self.active_qubits.update(term[1])
        self.parameter = [evolution_time]

    def apply_forward_gate(self, parameter, wavefunction):
        step_evolution_time=(parameter[0] + self.parameter[0])/self.n_trotter_step
        for _step in range(self.n_trotter_step):
            for i in range(len(self.qsubset_pauliword_list)):
                coeff, qsubset, pauliword = self.qsubset_pauliword_list[i]
                generalized_rotation(wavefunction, qsubset,
                                    pauliword, evolution_time=coeff*step_evolution_time)

    def apply_inverse_gate(self, parameter, wavefunction):
        step_evolution_time=(parameter[0] + self.parameter[0])/self.n_trotter_step
        for _step in range(self.n_trotter_step):
            for i in reversed(range(len(self.qsubset_pauliword_list))):
                coeff, qsubset, pauliword = self.qsubset_pauliword_list[i]
                generalized_rotation(wavefunction, qsubset,
                                    pauliword, evolution_time=-coeff*step_evolution_time)

    def get_gate_used(self):
        n_rotation = 0
        n_CNOT = 0
        for _ecoeff, qsubset, pauliword in self.qsubset_pauliword_list:
            n_rotation += count_single_gate_for_pauliword(pauliword)
            n_CNOT += 2 * (len(qsubset) - 1)
        n_rotation += 1
        return {"CNOT": n_CNOT*self.n_trotter_step, "SingleRotation": n_rotation*self.n_trotter_step}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Trotter_TimeEvolution: T=" + str(self.parameter[0])+" N_step:"+str(self.n_trotter_step)
        return info
