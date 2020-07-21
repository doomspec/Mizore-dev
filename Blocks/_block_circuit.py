from Blocks._block import Block
from Blocks._parametrized_circuit import ParametrizedCircuit
from ParameterOptimizer.ObjWrapper import evaluate_circuit_energy
from copy import copy

class BlockCircuit:
    """Circuit consists of blocks
    This class provides functions to produce ParametrizedCircuit for parameter optimizers to process. The users can easily fix some parameters while make the others adjustable.
    Attributes:
        block_list: The list of blocks contained in the circuit
        n_qubit: Number of qubits in the circuit
    """

    def __init__(self, n_qubit):
        self.block_list = []
        self.n_qubit = n_qubit
        return

    def add_block(self, block: Block):
        self.block_list.append(block)

    def count_n_parameter_by_position_list(self, position_list):
        n_parameter = 0
        for i in position_list:
            n_parameter += self.block_list[i].n_parameter
        return n_parameter

    def get_ansatz_by_position_list(self, position_list):
        """Return a ParametrizedCircuit with certain parameter adjustable
        Args:
            position_list: contains the indices of the block_list where the block's parameter is adjustable
        """
        def ansatz(parameter, wavefunction):
            para_index = 0
            for i in range(len(self.block_list)):
                block: Block = self.block_list[i]
                if i in position_list:
                    block.apply(
                        parameter[para_index:para_index+block.n_parameter], wavefunction)
                    para_index += block.n_parameter
                else:
                    block.apply(
                        [0.0]*block.n_parameter, wavefunction)
        return ParametrizedCircuit(ansatz,self.n_qubit,self.count_n_parameter_by_position_list(position_list))

    def get_ansatz_last_block(self):
        position_list = [len(self.block_list)-1]
        return self.get_ansatz_by_position_list(position_list)

    def get_ansatz(self):
        position_list = range(len(self.block_list))
        return self.get_ansatz_by_position_list(position_list)

    def get_fixed_parameter_ansatz(self):
        return self.get_ansatz_by_position_list([]).ansatz

    def get_energy(self, hamiltonian):
        ansatz = self.get_fixed_parameter_ansatz()
        return evaluate_circuit_energy([],self.n_qubit,hamiltonian,ansatz)
    
    def duplicate(self):
        copy_circuit=BlockCircuit(self.n_qubit)
        for block in self.block_list:
            copy_circuit.add_block(block)
        return copy_circuit

    def __str__(self):
        info=""
        if len(self.block_list)!=0:
            info+="Block Num:"+str(len(self.block_list))+"; Qubit Num:"+str(self.n_qubit)+"\n"
            info+="Block list:"+"\n"
            for block in self.block_list:
                info+=str(block)+"\n"
        else:
            info+="This is an Empty circuit. Qubit Num:"+str(self.n_qubit)+"\n"
        return info