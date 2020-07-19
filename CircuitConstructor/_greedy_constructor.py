from CircuitConstructor._circuit_constructor import *
from ParameterOptimizer._circuit_optimizer import basinhopping_optimizer
from Entanglers._entangler import Entangler
from multiprocessing import Process
from copy import copy, deepcopy
from Entanglers._utilities import *



class GreedyConstructor(CircuitConstructor):

    def __init__(self, n_qubit, hamiltonian, entangler_pool, max_n_entangler=100, terminate_energy=-NOT_DEFINED):

        Process.__init__(self)

        self.circuit = EntanglerCircuit(n_qubit)
        self.max_n_entangler = max_n_entangler
        self.terminate_energy = terminate_energy
        self.entangler_pool = entangler_pool
        self.n_qubit = n_qubit
        self.hamiltonian = hamiltonian

        return

    def run(self):
        print("Here is GreedyConstructor")
        print("Size of Entangler Pool:", len(self.entangler_pool.entanglers))
        #print(self.entangler_pool)
        self.init_energy = self.circuit.get_energy(self.hamiltonian)
        self.current_energy = self.init_energy
        print("Initial Energy:", self.init_energy)
        for layer in range(self.max_n_entangler):
            self.add_one_entangler()
            print(self.circuit)
            #print(concatenate_circuit(self.circuit,get_inverse_circuit(self.circuit)))
        return

    def add_one_entangler(self):
        trial_result_list = self.do_trial_on_entanglers()
        best_entangler = self.get_entangler_by_trial_result(trial_result_list)
        self.circuit.add_entangler(best_entangler)
        print("Entangler added, energy now is:", self.current_energy)
        return

    def do_trial_on_entanglers(self):
        trial_result_list = []
        for entangler in self.entangler_pool:
            trial_circuit = self.circuit.duplicate()
            trial_circuit.add_entangler(entangler)
            pcircuit = trial_circuit.get_ansatz_last_entangler()
            energy, amp = basinhopping_optimizer(
                pcircuit, self.hamiltonian)
            energy_descent = energy-self.current_energy
            trial_result_list.append((energy, energy_descent, amp, entangler))
        return trial_result_list

    def get_entangler_by_trial_result(self, trial_result_list):
        lowest_energy = NOT_DEFINED
        lowest_energy_index = -1
        for i in range(len(trial_result_list)):
            if trial_result_list[i][0] < lowest_energy:
                lowest_energy = trial_result_list[i][0]
                lowest_energy_index = i
        best_result = trial_result_list[lowest_energy_index]
        new_entangler = copy(best_result[3])
        new_entangler.parameter = best_result[2]
        self.current_energy = best_result[0]
        return new_entangler
