from Entanglers._entangler import Entangler
from Entanglers._parametrized_circuit import ParametrizedCircuit
from ParameterOptimizer.ObjWrapper import evaluate_circuit_energy
from copy import copy

class EntanglerCircuit:
    """Circuit consists of entanglers
    This class provides functions to produce ParametrizedCircuit for parameter optimizers to process. The users can easily fix some parameters while make the others adjustable.
    Attributes:
        entangler_list: The list of entanglers contained in the circuit
        n_qubit: Number of qubits in the circuit
    """

    entangler_list = list()
    n_qubit = -1

    def __init__(self, n_qubit):
        self.n_qubit = n_qubit
        return

    def add_entangler(self, entangler: Entangler):
        self.entangler_list.append(entangler)

    def count_n_parameter_by_position_list(self, position_list):
        n_parameter = 0
        for i in position_list:
            n_parameter += self.entangler_list[i].n_parameter
        return n_parameter

    def get_ansatz_by_position_list(self, position_list):
        """Return a ParametrizedCircuit with certain parameter adjustable
        Args:
            position_list: contains the indices of the entangler_list where the entangler's parameter is adjustable
        """
        def ansatz(parameter, wavefunction):
            para_index = 0
            for i in range(len(self.entangler_list)):
                entangler: Entangler = self.entangler_list[i]
                if i in position_list:
                    entangler.apply(
                        parameter[para_index:para_index+entangler.n_parameter], wavefunction)
                    para_index += entangler.n_parameter
                else:
                    entangler.apply(
                        [0.0]*entangler.n_parameter, wavefunction)
        return ParametrizedCircuit(ansatz,self.n_qubit,self.count_n_parameter_by_position_list(position_list))

    def get_ansatz_last_entangler(self):
        position_list = [len(self.entangler_list)-1]
        return self.get_ansatz_by_position_list(position_list)

    def get_ansatz(self):
        position_list = range(len(self.entangler_list))
        return self.get_ansatz_by_position_list(position_list)

    def get_fixed_parameter_ansatz(self):
        return self.get_ansatz_by_position_list([]).ansatz

    def get_energy(self, hamiltonian):
        ansatz = self.get_fixed_parameter_ansatz()
        return evaluate_circuit_energy([],self.n_qubit,hamiltonian,ansatz)
    
    def duplicate(self):
        copy_circuit=EntanglerCircuit(self.n_qubit)
        for entangler in self.entangler_list:
            copy_circuit.add_entangler(entangler)
        return copy_circuit

    def __str__(self):
        info=""
        if len(self.entangler_list)!=0:
            info+="Entangler Num:"+str(len(self.entangler_list))+"; Qubit Num:"+str(self.n_qubit)+"\n"
            info+="Entangler list:"+"\n"
            for entangler in self.entangler_list:
                info+=str(entangler)+"\n"
        else:
            info+="This is an Empty circuit. Qubit Num:"+str(self.n_qubit)+"\n"
        return info