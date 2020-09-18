from CircuitConstructor._no_parameter_constructor import NoParameterConstructor
from Objective._vqs_quality_obj import CircuitQualityObjective
from ParameterOptimizer import RealTimeEvolutionOptimizer
from ParameterOptimizer._rte_analytical_optimizer import RTEAnalyticalOptimizer
import time,json,pickle,os
from Blocks import TimeEvolutionBlock,BlockCircuit
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._trotter_evolution_block import TrotterTimeEvolutionBlock

class TimeEvolutionConstructor():

    def __init__(self, energy_obj, pool, init_circuit, project_name="Untitled",task_manager=None,is_analytical=False, n_block_per_iter=1,quality_cutoff=0.0001, diff=1e-4, n_circuit=3, stepsize=1e-3,delta_t=0.1):
        
        self.energy_obj = energy_obj
        self.circuit = init_circuit
        self.quality_cutoff = quality_cutoff
        self.pool = pool
        self.diff = diff
        self.delta_t=delta_t
        self.n_block_per_iter=n_block_per_iter
        self.is_analytical=is_analytical
        self.task_manager=task_manager
        self.quality_obj = CircuitQualityObjective(energy_obj, self.diff,is_analytical=is_analytical)
        self.n_circuit = n_circuit
        self.stepsize = stepsize

        if not is_analytical:
            self.evolver = RealTimeEvolutionOptimizer(random_adjust=0.0,
                                                  verbose=True,task_manager=task_manager, quality_cutoff=self.quality_cutoff, stepsize=self.stepsize, diff=self.diff,
                                                  calculate_quality=True, inverse_evolution=False)
        else:
            self.evolver = RTEAnalyticalOptimizer(random_adjust=0.0,
                                                  verbose=True,task_manager=task_manager, quality_cutoff=self.quality_cutoff, stepsize=self.stepsize,
                                                  calculate_quality=True, inverse_evolution=False)

        self.time_string = time.strftime(
            '%m-%d-%Hh%Mm%Ss', time.localtime(time.time()))
        self.project_name = project_name
        self.save_name = project_name+"_"+self.time_string
        self.save_path = "mizore_results/"+"adaptive_evolution/"+self.save_name
        self.save_self_info()

        self.quality_list=[]
        self.evolution_time_list=[]

        pass

    def run(self):

        circuit_list = [self.circuit.duplicate()]
        construct_needed = True
        total_time_evolved=0
        total_time_evolved_list=[]

        self.circuit.save_self_file(self.save_path,"0")

        while(True):

            if construct_needed:
                constructor = NoParameterConstructor(
                    self.quality_obj, self.pool, task_manager=self.task_manager,terminate_cost=self.quality_cutoff/2, init_circuit=self.circuit,n_block_per_iter=self.n_block_per_iter,not_save=True)
                new_circuit = constructor.run()
                if constructor.current_cost>self.quality_cutoff-1e-7:
                    print("Circuit constructor can not reach the object quality, consider using a larger pool!!!")
                    assert False
                new_circuit.set_all_block_active()
            else:
                new_circuit = self.circuit

            local_time_to_evolve = self.delta_t-(total_time_evolved % self.delta_t)
            print("local_time_to_evolve",local_time_to_evolve)

            new_circuit,evolved_time = self.evolver.do_time_evolution(
                new_circuit, self.energy_obj.hamiltonian, local_time_to_evolve)
            total_time_evolved+=evolved_time
            self.quality_list.extend(self.evolver.quality_list)
            #self.evolution_time_list.extend(self.evolver.evolution_time_list)
            print("Time evolved:",evolved_time)

            construct_needed = (evolved_time <= local_time_to_evolve-1e-7)

            if (not construct_needed) and (evolved_time>1e-7):
                circuit_list.append(new_circuit.duplicate())

                new_circuit.save_self_file(self.save_path,str(len(circuit_list)-1))

                total_time_evolved_list.append(total_time_evolved)
                print("Circuit added, time list:",total_time_evolved_list)
                for q in self.quality_list:
                    print(q)
            self.circuit = new_circuit
            if len(circuit_list) == self.n_circuit+1:
                return circuit_list
        
    def save_self_info(self):
        """
        Generate a log as a JSON file
        """
        mkdir(self.save_path)

        name_to_save=["project_name","n_block_per_iter","quality_cutoff","is_analytical","stepsize","delta_t"]
        log_dict = {}
        for key in name_to_save:
            log_dict[key]=self.__dict__[key]
        if not self.is_analytical:
            log_dict["diff"]=self.diff
        
        path = self.save_path + "/run_info.json"
        with open(path, "w") as f:
            json.dump(log_dict, f)
        path = self.save_path + "/energy_obj.pickle"
        with open(path, "wb") as f:
            pickle.dump(self.energy_obj, f)

def generate_benchmark(circuit_list,hamiltonian,delta_t):

    n_circuit=len(circuit_list)
    init_circuit=circuit_list[0]
    benchmark_circuits=[init_circuit]
    for step in range(1,n_circuit):
        bc=init_circuit.duplicate()
        bc.add_block(TimeEvolutionBlock(hamiltonian,init_angle=delta_t*step))
        benchmark_circuits.append(bc)
    fidelity_list=[0]*n_circuit
    fidelity_list[0]=1
    for step in range(1,n_circuit):
        fidelity_list[step]=abs(get_inner_two_circuit_product(circuit_list[step],benchmark_circuits[step]))

    return fidelity_list

def generate_trotter_benchmark_from_file(path,n_trotter_step):
    with open(path +"/energy_obj.pickle", "rb") as f:
        hamiltonian=pickle.load(f).hamiltonian

    with open(path + "/run_info.json", "r") as f:
        log_dict=json.load(f)

    delta_t=log_dict["delta_t"]
    circuit_path=path+"/0.bc"
    with open(circuit_path, "rb") as f:
        init_circuit=pickle.load(f)

    n_circuit=1
    while True:
        circuit_path=path+"/"+str(n_circuit)+".bc"
        if not os.path.exists(circuit_path):
            break
        n_circuit+=1

    return generate_trotter_benchmark(init_circuit,n_trotter_step,hamiltonian,delta_t,n_circuit)

def generate_trotter_benchmark(init_circuit,n_trotter_step,hamiltonian,delta_t,n_circuit):
    circuit_list=[init_circuit.duplicate()]
    for step in range(1,n_circuit):
        bc=init_circuit.duplicate()
        bc.add_block(TrotterTimeEvolutionBlock(hamiltonian,n_trotter_step=n_trotter_step*step,evolution_time=delta_t*step))
        circuit_list.append(bc)
    return generate_benchmark(circuit_list,hamiltonian,delta_t)

def generate_benchmark_from_file(path):

    with open(path +"/energy_obj.pickle", "rb") as f:
        hamiltonian=pickle.load(f).hamiltonian

    with open(path + "/run_info.json", "r") as f:
        log_dict=json.load(f)

    delta_t=log_dict["delta_t"]

    circuit_list=[]
    circuit_index=0
    while True:
        circuit_path=path+"/"+str(circuit_index)+".bc"
        if not os.path.exists(circuit_path):
            break
        with open(circuit_path, "rb") as f:
            step_circuit=pickle.load(f)
        circuit_list.append(step_circuit)
        circuit_index+=1
    #print(hamiltonian)
    #print("delta_t",delta_t)
    return generate_benchmark(circuit_list,hamiltonian,delta_t)    


def mkdir(path):
    is_dir_exists = os.path.exists(path)
    if not is_dir_exists:
        os.makedirs(path)
        return True
    else:
        return False