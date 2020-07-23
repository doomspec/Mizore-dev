from scipy.optimize import minimize, basinhopping
from ParameterOptimizer.ObjWrapper import get_obj_for_optimizer
from Utilities.Tools import random_list
from Blocks import BlockCircuit
from ParameterOptimizer import ParameterOptimizer
from Blocks._utilities import get_inner_two_circuit_product, get_circuit_energy
from scipy import linalg
import numpy

NOT_DEFINED=999999

class ImaginaryTimeEvolutionOptimizer(ParameterOptimizer):

    def __init__(self, random_adjust=0.01, diff=1e-4, stepsize=1e-1, n_step=10, max_increase_n_step=3, task_manager=None):
        ParameterOptimizer.__init__(self)

        self.random_adjust = random_adjust
        self.stepsize = stepsize
        self.diff = diff
        self.max_increase_n_step = max_increase_n_step
        self.energy_list=[]
        self.n_step=n_step
        self.lowest_energy=NOT_DEFINED
        self.lowest_energy_circuit=None

    def run_optimization(self, _circuit:BlockCircuit, hamiltonian):
        """
        Carry out ImaginaryTimeEvolution on the active positions of the BlockCircuit provided.
        """
        start_energy=get_circuit_energy(_circuit,hamiltonian)
        self.lowest_energy=start_energy
        self.lowest_energy_circuit=_circuit
        self.energy_list.append(start_energy)

        circuit=_circuit.duplicate()
        original_parameter=circuit.get_parameter_on_active_position()

        n_parameter = circuit.count_n_parameter_on_active_position()

        if n_parameter==0:
            #If active position list is empty, make all the position active
            circuit.active_position_list=list(range(len(circuit.block_list)))
            n_parameter=circuit.count_n_parameter_on_active_position()

        if self.random_adjust != 0:
            random_adjust_list = random_list(-self.random_adjust,
                                            self.random_adjust, n_parameter)
            circuit.adjust_parameter_on_active_position(random_adjust_list)
        
        
        previous_energy=self.lowest_energy
        increase_n_step=0

        for i in range(0, self.n_step):

            mat_A = [[0.0 for col in range(n_parameter)]
                     for row in range(n_parameter)]
            mat_C = [0.0 for col in range(n_parameter)]

            adjusted_circuits = []

            diff = self.diff
            for position in circuit.active_position_list:
                block_n_para=circuit.block_list[position].n_parameter
                for in_block_position in range(block_n_para):
                    adjust_list=[0.0]*block_n_para
                    adjust_list[in_block_position]+=diff
                    adjusted_circuit = circuit.duplicate()
                    adjusted_circuit.adjust_parameter_by_block_postion(adjust_list,position)
                    adjusted_circuits.append(adjusted_circuit)

            for i in range(n_parameter):
                for j in range(i, n_parameter):
                    inner_product1 = get_inner_two_circuit_product(
                        adjusted_circuits[i], adjusted_circuits[j])
                    inner_product2 = get_inner_two_circuit_product(
                        adjusted_circuits[i], circuit)
                    inner_product3 = get_inner_two_circuit_product(
                        circuit, adjusted_circuits[j])
                    term_value = inner_product1-inner_product2-inner_product3+1
                    term_value /= diff*diff
                    term_value = term_value.real
                    mat_A[i][j] = term_value
                    mat_A[j][i] = term_value

            #print(mat_A)

            origin_energy = get_circuit_energy(circuit, hamiltonian)
            for i in range(n_parameter):
                term_value = get_circuit_energy(
                    adjusted_circuits[i], hamiltonian)-origin_energy
                term_value /= diff
                term_value *= -0.5
                mat_C[i] = term_value

            #print(mat_C)

            try:
                ITE_derivative = linalg.solve(mat_A, mat_C)
            except linalg.LinAlgError:
                ITE_derivative = numpy.array(random_list(-self.random_adjust,
                                            self.random_adjust, n_parameter))

            ITE_derivative_norm = linalg.norm(ITE_derivative)
            ITE_derivative *= self.stepsize/ITE_derivative_norm
            circuit.adjust_parameter_on_active_position(ITE_derivative)

            energy=get_circuit_energy(circuit, hamiltonian)
            self.energy_list.append(energy)

            if energy<self.lowest_energy:
                self.lowest_energy=energy
                self.lowest_energy_circuit=circuit

            if energy>=previous_energy:
                increase_n_step+=1

            previous_energy=energy
            print(self.lowest_energy,self.energy_list)

            if increase_n_step>=self.max_increase_n_step:
                break
        optimal_parameter=self.lowest_energy_circuit.get_parameter_on_active_position()
        amp=[]
        for i in range(len(original_parameter)):
            amp.append(optimal_parameter[i]-original_parameter[i])
        #print(original_parameter,optimal_parameter,amp)
        return self.lowest_energy,amp