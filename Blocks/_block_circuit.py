from Blocks._block import Block
from Blocks._parametrized_circuit import ParametrizedCircuit
from copy import copy, deepcopy


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
        self.active_position_list = []
        return

    def add_block(self, block: Block):
        self.block_list.append(block)

    def count_n_parameter_by_position_list(self, position_list):
        n_parameter = 0
        for i in position_list:
            n_parameter += self.block_list[i].n_parameter
        return n_parameter

    def count_n_parameter_on_active_position(self):
        return self.count_n_parameter_by_position_list(self.active_position_list)

    def count_n_parameter(self):
        position_list = list(range(len(self.block_list)))
        return self.count_n_parameter_by_position_list(position_list)

    def get_parameter_on_position_list(self, position_list):
        para_list = []
        for position in position_list:
            para_list.extend(self.block_list[position].parameter)
        return para_list

    def get_parameter_on_active_position(self):
        return self.get_parameter_on_position_list(self.active_position_list)

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
                        parameter[para_index:para_index + block.n_parameter], wavefunction)
                    para_index += block.n_parameter
                else:
                    block.apply(
                        [0.0] * block.n_parameter, wavefunction)

        return ParametrizedCircuit(ansatz, self.n_qubit, self.count_n_parameter_by_position_list(position_list))

    def get_ansatz_on_active_position(self):
        return self.get_ansatz_by_position_list(self.active_position_list)

    def get_ansatz_last_block(self):
        position_list = [len(self.block_list) - 1]
        return self.get_ansatz_by_position_list(position_list)

    def set_only_last_block_active(self):
        self.active_position_list = [len(self.block_list) - 1]

    def get_active_n_parameter(self):
        return self.count_n_parameter_by_position_list(self.active_position_list)

    def get_ansatz(self):
        position_list = list(range(len(self.block_list)))
        return self.get_ansatz_by_position_list(position_list)

    def get_fixed_parameter_ansatz(self):
        return self.get_ansatz_by_position_list([]).ansatz

    def adjust_parameter_by_para_postion(self, adjust_value, position):
        n_parameter = 0
        block_postion = 0
        in_block_position = 0
        for i in range(len(self.block_list)):
            n_parameter += self.block_list[i].n_parameter
            if n_parameter > position:
                block_postion = i
                in_block_position = self.block_list[i].n_parameter - n_parameter + position
                break
        self.block_list[block_postion].parameter[in_block_position] += adjust_value
        return

    def adjust_parameter_by_block_postion(self, adjust_list, position):
        # To be improved
        self.adjust_parameter_by_block_postion_list(adjust_list, (position,))

    def adjust_parameter_by_block_postion_list(self, adjust_list, position_list):
        if len(adjust_list) != self.count_n_parameter_by_position_list(position_list):
            raise Exception(
                "The number of parameters provided does not match the circuit!")

        para_index = 0
        for position in position_list:
            for in_block_position in range(self.block_list[position].n_parameter):
                self.block_list[position].parameter[in_block_position] += adjust_list[para_index]
                para_index += 1
        return

    def adjust_parameter_on_active_position(self, adjust_list):
        self.adjust_parameter_by_block_postion_list(adjust_list, self.active_position_list)

    def adjust_all_parameter_by_list(self, adjust_list):

        if len(adjust_list) != self.count_n_parameter():
            raise Exception(
                "The number of parameters provided does not match the circuit!")
        para_index = 0
        for block_postion in range(len(self.block_list)):
            n_block_para = self.block_list[block_postion].n_parameter
            for in_block_position in range(n_block_para):
                self.block_list[block_postion].parameter[in_block_position] += adjust_list[para_index]
                para_index += 1
        return

    def duplicate(self):
        copy_circuit = BlockCircuit(self.n_qubit)
        for block in self.block_list:
            copy_circuit.add_block(deepcopy(block))
        copy_circuit.active_position_list = self.active_position_list
        return copy_circuit

    def __str__(self):
        info = ""
        if len(self.block_list) != 0:
            info += "Block Num:" + str(len(self.block_list)) + "; Qubit Num:" + str(self.n_qubit) + "\n"
            info += "Block list:" + "\n"
            for block in self.block_list:
                info += str(block) + "\n"
        else:
            info += "This is an Empty circuit. Qubit Num:" + str(self.n_qubit) + "\n"
        return info
