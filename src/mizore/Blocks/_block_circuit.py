from ._block import Block
from ._parametrized_circuit import ParametrizedCircuit
from copy import copy, deepcopy


class BlockCircuit:
    """
    Circuit consists of blocks. 
    Blocks are listed in self.block_list to form a circuit. 

    And the class provides functions to produce ParametrizedCircuit for parameter optimizers to process. 
    The users can easily fix some parameters while make the others adjustable.

    Especially, in self.active_position_list records the indices of blocks in self.block_list
    whose parameter should be adjustable.

    One can make use of duplicate() to duplicate a circuit

    Attributes:
        block_list: The list of blocks contained in the circuit
        n_qubit: Number of qubits in the circuit
    """

    def __init__(self, n_qubit, init_block=None):
        self.block_list = []
        self.n_qubit = n_qubit
        self.active_position_list = []
        self.qubit_index_mapping = None
        self.add_block(init_block)

        return

    def add_block(self, block: Block):
        if block != None:
            self.block_list.append(copy(block))
            self.active_position_list.append(len(self.block_list) - 1)

    def remove_block(self, position):
        self.active_position_list.remove(len(self.block_list) - 1)
        self.block_list.remove(self.block_list[position])

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
        if self.qubit_index_mapping == None:
            return self._get_ansatz_by_position_list_0(position_list)
        else:
            return self._get_ansatz_by_position_list_with_qubit_mapping(position_list, self.qubit_index_mapping)

    def _get_ansatz_by_position_list_0(self, position_list):
        """
        Return a ParametrizedCircuit with certain parameter adjustable
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

    def _get_ansatz_by_position_list_with_qubit_mapping(self, position_list, qubit_index_mapping):
        # print(qubit_index_mapping)
        if not qubit_index_mapping:  # If no active qubit
            def ansatz0(parameter, wavefunction):
                pass

            return ParametrizedCircuit(ansatz0, 0, 0)

        redundant_n_qubit = qubit_index_mapping[len(qubit_index_mapping) - 1] + 1

        def ansatz(parameter, wavefunction):
            mapped_wavefunction = [None] * redundant_n_qubit
            for i in range(len(qubit_index_mapping)):
                mapped_wavefunction[qubit_index_mapping[i]] = wavefunction[i]
                # print(mapped_wavefunction)
            para_index = 0
            for i in range(len(self.block_list)):
                block: Block = self.block_list[i]
                if i in position_list:
                    block.apply(
                        parameter[para_index:para_index + block.n_parameter], mapped_wavefunction)
                    para_index += block.n_parameter
                else:
                    block.apply(
                        [0.0] * block.n_parameter, mapped_wavefunction)

        return ParametrizedCircuit(ansatz, len(qubit_index_mapping),
                                   self.count_n_parameter_by_position_list(position_list))

    def get_ansatz_on_active_position(self):
        return self.get_ansatz_by_position_list(self.active_position_list)

    def get_ansatz_last_block(self):
        position_list = [len(self.block_list) - 1]
        return self.get_ansatz_by_position_list(position_list)

    def set_only_last_block_active(self):
        self.active_position_list = [len(self.block_list) - 1]

    def set_all_block_active(self):
        self.active_position_list = list(range(len(self.block_list)))

    def get_active_n_parameter(self):
        return self.count_n_parameter_by_position_list(self.active_position_list)

    def get_ansatz(self):
        position_list = list(range(len(self.block_list)))
        return self.get_ansatz_by_position_list(position_list)

    def get_fixed_parameter_ansatz(self):
        return self.get_ansatz_by_position_list([])

    def adjust_parameter_by_para_postion(self, adjust_value, position):
        n_parameter = 0
        block_postion = 0
        in_block_position = 0
        for i in range(len(self.block_list)):
            n_parameter += self.block_list[i].n_parameter
            if n_parameter > position:
                block_postion = i
                in_block_position = self.block_list[i].n_parameter - \
                                    n_parameter + position
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
        self.adjust_parameter_by_block_postion_list(
            adjust_list, self.active_position_list)

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

    def get_gate_used(self):
        gate_used = {"CNOT": 0, "SingleRotation": 0, "TimeEvolution": 0}
        for block in self.block_list:
            block_gate = block.get_gate_used()
            for key in block_gate.keys():
                gate_used[key] += block_gate[key]
        return gate_used

    def duplicate(self):
        copy_circuit = BlockCircuit(self.n_qubit)
        for block in self.block_list:
            copy_circuit.add_block(deepcopy(block))
        copy_circuit.active_position_list = self.active_position_list
        return copy_circuit

    def get_active_qubits(self):
        active_qubits = set()
        for block in self.block_list:
            active_qubits.update(block.get_active_qubits())
        if not active_qubits:  # If active_qubits is empty
            for block in self.block_list:
                active_qubits.update(block.qsubset)
        return active_qubits

    def get_disjoint_active_sets(self):
        from ..Utilities.UnionFind import UnionFind
        uf = UnionFind(list(range(self.n_qubit)))
        for block in self.block_list:
            uf.union_list(block.get_active_qubits())
        return uf.components()

    def avoid_redundant_qubit(self):
        active_qubits = list(self.get_active_qubits())
        active_qubits.sort()
        self.qubit_index_mapping = active_qubits
        self.active_position_list = list(
            set(self.active_position_list).intersection(list(range(len(self.block_list)))))
        self.active_position_list.sort()
        # print(self.qubit_index_mapping)

    
    def apply(self,wavefunction):
        for block in self.block_list:
            block.apply([0]*block.n_parameter,wavefunction)

    def __str__(self):
        info = ""
        if len(self.block_list) != 0:
            info += "Block Num:" + str(len(self.block_list)) + \
                    "; Qubit Num:" + str(self.n_qubit) + "\n"
            info += "Block list:"
            for block in self.block_list:
                info += "\n" + str(block)
        else:
            info += "\n" + "This is an Empty circuit. Qubit Num:" + \
                    str(self.n_qubit)
        return info

    def save_self_file(self,path,name):
        save_circuit(self,path,name)

    def read_from_file(self,path):
        self=read_circuit(path)

import pickle,os

def mkdir(path):
    is_dir_exists = os.path.exists(path)
    if not is_dir_exists:
        os.makedirs(path)
        return True
    else:
        return False

def read_circuit(path):
    with open(path, "rb") as f:
        bc: BlockCircuit = pickle.load(f)
    return bc

def save_circuit(circuit,path,name):
    mkdir(path)
    full_path=path+"/"+name+".bc"
    with open(full_path, "wb") as f:
        pickle.dump(circuit, f)