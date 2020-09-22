from ._no_parameter_constructor import NoParameterConstructor
from ParameterOptimizer._vqs_utilities import *

class AnalyticalRTSConstructor(NoParameterConstructor):

    CONSTRUCTOR_NAME = "AnalyticalRTSConstructor"

    def __init__(self, *args, **kwargs):
        NoParameterConstructor.__init__(self,*args,**kwargs)
        return
    
    def get_current_cost(self):
        if self.circuit.count_n_parameter_on_active_position()>1:
            return calc_quality_derivative_by_obj_parallel_ana(self.task_manager,self.cost,self.circuit)
        else:
            return NoParameterConstructor.get_current_cost(self)
    """
    def do_trial_on_circuits_by_cost_gradient(self, trial_circuits=None):
        if trial_circuits == None:
            trial_circuits = self.trial_circuits
        
        quality_list=calc_quality_of_many_circuits_parallel(self.task_manager,trial_circuits,self.cost.hamiltonian_mat,self.cost.hamiltonian_square)

        trial_result_list=[]
        for i in range(len(trial_circuits)):
            cost = quality_list[i]
            cost_descent = self.current_cost - cost
            # See whether the new entangler decreases the cost
            if cost_descent > 1e-12:
                trial_result_list.append((cost, trial_circuits[i]))
        
        return trial_result_list
    """

def calc_quality_of_many_circuits_parallel(task_manager,trial_circuits,hamiltonian_mat,hamiltonian_square):
    n_trial_circuit=len(trial_circuits)

    mat_C_task_id_list=[]
    mat_A_task_id_list=[]

    for trial_circuit in trial_circuits:
        trail_derivative_circuits=get_derivative_circuit(trial_circuit)
        mat_C_task_id=add_calc_C_mat_analytical_task(task_manager,hamiltonian_mat,trial_circuit,trail_derivative_circuits)
        task_manager.flush(task_package_size=100)
        mat_A_task_id=add_calc_A_mat_analytical_tasks(task_manager,trial_circuit,trail_derivative_circuits)
        task_manager.flush(task_package_size=100)
        mat_C_task_id_list.append(mat_C_task_id)
        mat_A_task_id_list.append(mat_A_task_id)

    mat_C_result_list=[]
    mat_A_result_list=[]
    n_parameter=trial_circuits[0].count_n_parameter_on_active_position()

    for mat_C_task_id in mat_C_task_id_list:
        mat_C=np.imag(task_manager.receive_task_result(task_series_id=mat_C_task_id)[0])
        print(mat_C)
        mat_C_result_list.append(mat_C)

    for mat_A_task_id in mat_A_task_id_list:
        mat_A=np.real(calc_A_mat_analytical_by_task_results(task_manager,mat_A_task_id,n_parameter))
        print(mat_A)
        mat_A_result_list.append(mat_A)
    
    quality_list=[]
    derivative_list=[]
    
    for i in range(n_trial_circuit):
        derivative_list.append(calc_derivative(mat_A_result_list[i],mat_C_result_list[i]))

    for trial_circuit in trial_circuits:
        quality=calc_RTE_quality(hamiltonian_square,mat_A_result_list[i],mat_C_result_list[i],derivative_list[i],trial_circuit)
        print(quality)
        quality_list.append(quality)

    return quality_list
