from ._imaginary_time_evolution_optimizer import *
from Utilities.Tools import qubit_operator2matrix,random_list
from Blocks._utilities import get_circuit_complete_amplitudes, evaluate_off_diagonal_term_by_amps,get_circuit_energy,get_inner_two_circuit_product

class RealTimeEvolutionOptimizer(ImaginaryTimeEvolutionOptimizer):

    def __init__(self, quality_cutoff=99999,*args,**kwargs):
        ImaginaryTimeEvolutionOptimizer.__init__(self, *args, **kwargs)
        self.hamiltonian_mat = None
        self.calculate_quality=True
        self.adjusted_original_inner_product_list = None
        self.quality_cutoff=quality_cutoff
        self.get_best_result = False
        self.quality_list=[]
        self.evolution_time_list=[]

    def calc_derivative(self, circuit, hamiltonian):
        adjusted_circuits = get_adjusted_circuit(self.diff,circuit)
        n_parameter = len(adjusted_circuits)
        mat_B = calc_B_mat(circuit, adjusted_circuits)
        mat_C = np.imag(self.calc_C_mat(circuit, adjusted_circuits, hamiltonian))
        mat_A = np.real(self.calc_A_mat(circuit, adjusted_circuits, mat_B))
        try:
            derivative = linalg.solve(mat_A, mat_C)
        except linalg.LinAlgError:
            derivative = np.array(random_list(-self.random_adjust,
                                                 self.random_adjust, n_parameter))
 
        quality=self.calc_quality(mat_A,mat_C,derivative,circuit)

        return derivative,quality

    def calc_C_mat(self, circuit, adjusted_circuits, hamiltonian):
        if self.hamiltonian_mat is None:
            self.hamiltonian_mat = qubit_operator2matrix(
                circuit.n_qubit, hamiltonian)
        return calc_C_mat_by_hamiltonian_mat(self.hamiltonian_mat,self.diff,circuit,adjusted_circuits)

    def calc_quality(self,mat_A,mat_C,derivative,circuit):
        return calc_RTE_quality(self.hamiltonian_square,mat_A,mat_C,derivative,circuit)


    def run_optimization(self, _circuit: BlockCircuit, hamiltonian,n_step):
        print("Unfinished")
        assert False
        if self.hamiltonian_square is None:
            self.hamiltonian_square = hamiltonian*hamiltonian
            self.hamiltonian_square.compress()

        circuit = _circuit.duplicate()
        
        n_parameter = circuit.count_n_parameter_on_active_position()
        
        evolved_time=0
        if n_parameter == 0:
            # If active position list is empty, make all the position active
            circuit.active_position_list = list(range(len(circuit.block_list)))
            n_parameter = circuit.count_n_parameter_on_active_position()

        if self.random_adjust != 0:
            random_adjust_list = random_list(-self.random_adjust,
                                             self.random_adjust, n_parameter)
            circuit.adjust_parameter_on_active_position(random_adjust_list)

        for n_step_evolved in range(0, n_step):
            derivative,quality = self.calc_derivative(circuit, hamiltonian)
            if quality>=self.quality_cutoff:
                break
            derivative_norm = linalg.norm(derivative)
            delta_t_evolve=self.stepsize/derivative_norm
            para_shift = derivative * delta_t_evolve
            evolved_time+=delta_t_evolve
            if self.inverse_evolution:
                para_shift = -1 * para_shift
            circuit.adjust_parameter_on_active_position(para_shift)


        return circuit,evolved_time,n_step_evolved

    def do_time_evolution(self, _circuit: BlockCircuit, hamiltonian, evolution_time, max_n_step=100):

        if self.hamiltonian_square is None:
            self.hamiltonian_square = hamiltonian*hamiltonian
            self.hamiltonian_square.compress()

        circuit = _circuit.duplicate()
        n_parameter = circuit.count_n_parameter_on_active_position()
        self.evolution_time_list=[]
        self.quality_list=[]

        if n_parameter == 0:
            # If active position list is empty, make all the position active
            circuit.active_position_list = list(range(len(circuit.block_list)))
            n_parameter = circuit.count_n_parameter_on_active_position()

        evolved_time=0
        n_step=0

        while True:
            derivative,quality = self.calc_derivative(circuit, hamiltonian)
            if quality>=self.quality_cutoff:
                break
            
            derivative_norm = linalg.norm(derivative)
            delta_t_evolve=self.stepsize/derivative_norm

            if evolved_time+delta_t_evolve>=evolution_time:
                delta_t_evolve=evolution_time-evolved_time
            
            para_shift = derivative * (-1*delta_t_evolve)
            evolved_time+=delta_t_evolve

            self.evolution_time_list.append(evolved_time)
            self.quality_list.append(quality)

            n_step+=1
            if self.inverse_evolution:
                para_shift = -1 * para_shift
            circuit.adjust_parameter_on_active_position(para_shift)
            if evolved_time>=evolution_time-1e-7:
                break
            if n_step>=max_n_step:
                print("ATTENTION: n_step>=max_n_step !")
                break

        self.evolution_time_list=np.array(self.evolution_time_list)
        self.quality_list=np.array(self.quality_list)

        return circuit,evolved_time