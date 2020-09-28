from CircuitConstructor._no_parameter_constructor import NoParameterConstructor
from CircuitConstructor._analytical_rts_constructor import AnalyticalRTSConstructor
from Objective._vqs_quality_obj import CircuitQualityObjective
from ParameterOptimizer import RealTimeEvolutionOptimizer
from ParameterOptimizer._rte_analytical_optimizer import RTEAnalyticalOptimizer
import time
import json
import pickle
import os
from Blocks import TimeEvolutionBlock, BlockCircuit
from Blocks._utilities import get_inner_two_circuit_product
from Blocks._trotter_evolution_block import TrotterTimeEvolutionBlock
import numpy as np


class TimeEvolutionConstructor():

    def __init__(self, energy_obj, pool, init_circuit, project_name="Untitled", task_manager=None, is_analytical=False, n_block_per_iter=1, quality_cutoff=0.0001, diff=1e-4, n_circuit=3, stepsize=1e-3, delta_t=0.1, special_save_name = None, always_active_blocks=None,n_extra_active_blocks=-1):

        self.energy_obj = energy_obj
        self.n_qubit = energy_obj.n_qubit
        self.circuit = init_circuit
        self.quality_cutoff = quality_cutoff
        self.pool = pool
        self.diff = diff
        self.delta_t = delta_t
        self.n_block_per_iter = n_block_per_iter
        self.is_analytical = is_analytical
        self.task_manager = task_manager
        self.quality_obj = CircuitQualityObjective(
            energy_obj.n_qubit, energy_obj.hamiltonian, self.diff, is_analytical=is_analytical)
        self.n_circuit = n_circuit
        self.stepsize = stepsize
        
        self.always_active_blocks=always_active_blocks
        self.n_extra_active_blocks=n_extra_active_blocks

        if not is_analytical:
            self.evolver = RealTimeEvolutionOptimizer(random_adjust=0.0,
                                                      verbose=True, task_manager=task_manager, quality_cutoff=self.quality_cutoff, stepsize=self.stepsize, diff=self.diff,
                                                      calculate_quality=True, inverse_evolution=False)
        else:
            self.evolver = RTEAnalyticalOptimizer(random_adjust=0.0,
                                                  verbose=True, task_manager=task_manager, quality_cutoff=self.quality_cutoff, stepsize=self.stepsize,
                                                  calculate_quality=True, inverse_evolution=False)

        self.time_string = time.strftime(
            '%m-%d-%Hh%Mm%Ss', time.localtime(time.time()))
        self.project_name = project_name
        if special_save_name==None:
            self.save_name = project_name+"_"+self.time_string
        else:
            self.save_name = special_save_name
        self.save_path = "mizore_results/"+"adaptive_evolution/"+self.save_name
        self.save_self_info()

        self.quality_list = []
        self.evolution_time_list = []
        self.n_block_change = []
        self.total_time_evolved = 0

        self.circuit_list = [self.circuit.duplicate()]
        self.total_time_evolved = 0
        self.circuit.save_self_file(self.save_path, "0")

        pass

    def get_circuit_constructor(self):
        return self.get_circuit_constructor_by_quality_obj(self.quality_obj)

    def get_circuit_constructor_by_quality_obj(self, quality_obj):
        if self.is_analytical:
            return AnalyticalRTSConstructor(
                quality_obj, self.pool, task_manager=self.task_manager, terminate_cost=self.quality_cutoff/2, init_circuit=self.circuit, n_block_per_iter=self.n_block_per_iter, not_save=True,always_active_blocks=self.always_active_blocks,n_extra_active_blocks=self.n_extra_active_blocks)
        else:
            return NoParameterConstructor(
                quality_obj, self.pool, task_manager=self.task_manager, terminate_cost=self.quality_cutoff/2, init_circuit=self.circuit, n_block_per_iter=self.n_block_per_iter, not_save=True,always_active_blocks=self.always_active_blocks,n_extra_active_blocks=self.n_extra_active_blocks)

    def get_circuit_constructor_by_hamiltonian(self, hamiltonian):
        quality_obj = CircuitQualityObjective(self.n_qubit,
                                              hamiltonian, self.diff, is_analytical=self.is_analytical)
        return self.get_circuit_constructor_by_quality_obj(quality_obj)

    def evolve(self, circuit, time):
        return self.evolver.do_time_evolution(
            circuit, self.energy_obj.hamiltonian, time)

    def run(self, construct_first=True):

        last_evolved_time = -1
        total_time_evolved_list = []
        construct_needed = construct_first  # Default to be True

        while(True):

            if construct_needed:
                constructor = self.get_circuit_constructor()
                new_circuit = constructor.run()
                if constructor.current_cost > self.quality_cutoff-1e-10:
                    print(
                        "Circuit constructor can not reach the object quality, consider using a larger pool!!!")
                    assert False
                new_circuit.set_all_block_active()
                self.n_block_change.append((self.total_time_evolved, len(
                    new_circuit.block_list), new_circuit.get_gate_used()))
            else:
                new_circuit = self.circuit

            local_time_to_evolve = self.delta_t - \
                (self.total_time_evolved % self.delta_t)
            if local_time_to_evolve < 1e-12:
                local_time_to_evolve = self.delta_t

            print("local_time_to_evolve", local_time_to_evolve)

            new_circuit, evolved_time = self.evolve(
                new_circuit, local_time_to_evolve)

            self.quality_list = np.append(
                self.quality_list, self.evolver.quality_list)
            self.evolution_time_list = np.append(
                self.evolution_time_list, self.total_time_evolved+self.evolver.evolution_time_list)

            self.total_time_evolved += evolved_time

            print("Time evolved:", evolved_time)

            construct_needed = (
                abs(evolved_time-local_time_to_evolve) >= 1e-10)

            if ((not construct_needed) and (self.total_time_evolved > last_evolved_time)):
                self.circuit_list.append(new_circuit.duplicate())
                last_evolved_time = self.total_time_evolved
                new_circuit.save_self_file(
                    self.save_path, str(len(self.circuit_list)-1))
                self.save_run_status_info()
                total_time_evolved_list.append(self.total_time_evolved)
                print("Circuit added, time list:", total_time_evolved_list)

            self.circuit = new_circuit
            if len(self.circuit_list) == self.n_circuit+1:
                return self.circuit_list

    def save_self_info(self):
        """
        Generate a log as a JSON file
        """
        mkdir(self.save_path)

        name_to_save = ["project_name", "n_block_per_iter",
                        "quality_cutoff", "is_analytical", "stepsize", "delta_t","always_active_blocks","n_extra_active_blocks"]
        log_dict = {}
        for key in name_to_save:
            log_dict[key] = self.__dict__[key]
        if not self.is_analytical:
            log_dict["diff"] = self.diff

        path = self.save_path + "/run_info.json"
        with open(path, "w") as f:
            json.dump(log_dict, f)
        path = self.save_path + "/energy_obj.pickle"
        with open(path, "wb") as f:
            pickle.dump(self.energy_obj, f)
        path = self.save_path + "/pool.pickle"
        with open(path, "wb") as f:
            pickle.dump(self.pool, f)

    def get_run_status_info_dict(self):
        log_dict = {}
        log_dict["n_block_change"] = self.n_block_change
        log_dict["quality_list"] = self.quality_list.tolist()
        log_dict["evolution_time_list"] = self.evolution_time_list.tolist()
        return log_dict

    def save_run_status_info(self):
        path = self.save_path + "/run_status_info.json"
        with open(path, "w") as f:
            json.dump(self.get_run_status_info_dict(), f)


def resume_run_from_file(path, pool, task_manager, n_circuit):

    with open(path + "/energy_obj.pickle", "rb") as f:
        energy_obj = pickle.load(f)
    with open(path + "/run_info.json", "r") as f:
        log_dict = json.load(f)
    with open(path + "/run_status_info.json", "r") as f:
        status_dict = json.load(f)

    circuit_list = read_circuits_from_file(path)
    project_name = path.split("/")[-1]
    constructor = TimeEvolutionConstructor(energy_obj, pool, circuit_list[-1], log_dict["project_name"], task_manager, log_dict["is_analytical"],
                                           log_dict["n_block_per_iter"], log_dict["quality_cutoff"], None, len(circuit_list)+n_circuit, log_dict["stepsize"], log_dict["delta_t"],log_dict["always_active_blocks",log_dict["n_extra_active_blocks"]])
    constructor.circuit_list = circuit_list
    constructor.total_time_evolved = (len(circuit_list)-1)*log_dict["delta_t"]
    old_save_path_split = constructor.save_path.split("/")
    old_save_path_split[-1] = project_name
    new_save_path = "/".join(old_save_path_split)
    constructor.save_path = new_save_path
    print("Resume from circuit:")
    print(circuit_list[-1])
    constructor.n_block_change = status_dict["n_block_change"]
    constructor.quality_list = np.array(status_dict["quality_list"])
    constructor.evolution_time_list = np.array(
        status_dict["evolution_time_list"])

    constructor.run(construct_first=False)


def generate_benchmark_for_compare(circuit_list_list, hamiltonian, delta_t, task_manager=None):
    if task_manager is None:
        return generate_benchmark_for_compare_0(circuit_list_list, hamiltonian, delta_t)
    else:
        return generate_benchmark_for_compare_parallel(circuit_list_list, hamiltonian, delta_t, task_manager)


def generate_benchmark_for_compare_parallel(circuit_list_list, hamiltonian, delta_t, task_manager):
    from ParallelTaskRunner import InnerProductTask
    list_n_circuit = [len(circuit_list) for circuit_list in circuit_list_list]
    init_circuit = circuit_list_list[0][0]
    benchmark_circuits = [init_circuit]
    for step in range(1, max(list_n_circuit)):
        bc = init_circuit.duplicate()
        bc.add_block(TimeEvolutionBlock(hamiltonian, init_angle=delta_t*step))
        benchmark_circuits.append(bc)
    fidelity_list_list = []
    task_series_id = "Benchmark" + str(time.time() % 10000)
    for i in range(len(circuit_list_list)):
        for step in range(1, list_n_circuit[i]):
            task_manager.add_task_to_buffer(InnerProductTask(
                circuit_list_list[i][step], benchmark_circuits[step]), task_series_id=task_series_id)
    task_manager.flush()
    res_list = task_manager.receive_task_result(
        task_series_id=task_series_id, progress_bar=True)
    task_index = 0
    for i in range(len(circuit_list_list)):
        fidelity_list = [0]*list_n_circuit[i]
        fidelity_list[0] = 1
        for step in range(1, list_n_circuit[i]):
            fidelity_list[step] = abs(res_list[task_index])
            task_index += 1
        fidelity_list_list.append(fidelity_list)
    return fidelity_list_list


def generate_benchmark_for_compare_0(circuit_list_list, hamiltonian, delta_t):
    list_n_circuit = [len(circuit_list) for circuit_list in circuit_list_list]
    init_circuit = circuit_list_list[0][0]
    benchmark_circuits = [init_circuit]
    for step in range(1, max(list_n_circuit)):
        bc = init_circuit.duplicate()
        bc.add_block(TimeEvolutionBlock(hamiltonian, init_angle=delta_t*step))
        benchmark_circuits.append(bc)
    fidelity_list_list = []
    for i in range(len(circuit_list_list)):
        fidelity_list = [0]*list_n_circuit[i]
        fidelity_list[0] = 1
        for step in range(1, list_n_circuit[i]):
            fidelity_list[step] = abs(get_inner_two_circuit_product(
                circuit_list_list[i][step], benchmark_circuits[step]))
        fidelity_list_list.append(fidelity_list)
    return fidelity_list_list


def generate_benchmark(circuit_list, hamiltonian, delta_t, task_manager=None):
    return generate_benchmark_for_compare([circuit_list], hamiltonian, delta_t, task_manager=task_manager)[0]


def generate_trotter_benchmark_from_file(path, n_trotter_step):
    with open(path + "/energy_obj.pickle", "rb") as f:
        hamiltonian = pickle.load(f).hamiltonian

    with open(path + "/run_info.json", "r") as f:
        log_dict = json.load(f)

    delta_t = log_dict["delta_t"]
    circuit_path = path+"/0.bc"
    with open(circuit_path, "rb") as f:
        init_circuit = pickle.load(f)

    n_circuit = 1
    while True:
        circuit_path = path+"/"+str(n_circuit)+".bc"
        if not os.path.exists(circuit_path):
            break
        n_circuit += 1

    return generate_trotter_benchmark(init_circuit, n_trotter_step, hamiltonian, delta_t, n_circuit)


def generate_trotter_benchmark_circuits(init_circuit, n_trotter_step, hamiltonian, delta_t, n_circuit):
    circuit_list = [init_circuit.duplicate()]
    for step in range(1, n_circuit):
        bc = init_circuit.duplicate()
        bc.add_block(TrotterTimeEvolutionBlock(
            hamiltonian, n_trotter_step=n_trotter_step*step, evolution_time=delta_t*step))
        circuit_list.append(bc)
    return circuit_list


def generate_trotter_benchmark(init_circuit, n_trotter_step, hamiltonian, delta_t, n_circuit):
    circuit_list = generate_trotter_benchmark_circuits(
        init_circuit, n_trotter_step, hamiltonian, delta_t, n_circuit)
    return generate_benchmark(circuit_list, hamiltonian, delta_t)


def generate_benchmark_from_file(path):

    with open(path + "/energy_obj.pickle", "rb") as f:
        hamiltonian = pickle.load(f).hamiltonian

    with open(path + "/run_info.json", "r") as f:
        log_dict = json.load(f)

    delta_t = log_dict["delta_t"]

    circuit_list = read_circuits_from_file(path)

    return generate_benchmark(circuit_list, hamiltonian, delta_t)


def read_circuits_from_file(path, delta_n=1):
    circuit_list = []
    circuit_index = 0
    while True:
        circuit_path = path+"/"+str(circuit_index)+".bc"
        if not os.path.exists(circuit_path):
            break
        with open(circuit_path, "rb") as f:
            step_circuit = pickle.load(f)
        circuit_list.append(step_circuit)
        circuit_index += delta_n
    return circuit_list


def draw_run_status_figure(path):

    with open(path + "/energy_obj.pickle", "rb") as f:
        hamiltonian = pickle.load(f).hamiltonian
    with open(path + "/run_status_info.json", "r") as f:
        log_dict = json.load(f)
    n_block_change = log_dict["n_block_change"]
    gate_name = "CNOT"
    n_gate_list = []
    n_gate_time_list = []
    for item in n_block_change:
        n_gate_time_list.append(item[0])
        n_gate_list.append(item[2][gate_name])
    quality_list = log_dict["quality_list"]
    evolution_time_list = log_dict["evolution_time_list"]
    first_trotter_gate_use = TrotterTimeEvolutionBlock(
        hamiltonian, n_trotter_step=1, evolution_time=0.1).get_gate_used()[gate_name]
    end_time = evolution_time_list[-1]
    import matplotlib
    import matplotlib.pyplot as plt

    gate_name = "CNOT"
    n_gate_list = []
    n_gate_time_list = []
    n_block_change.append((end_time, None, None))
    for i in range(len(n_block_change)-1):
        n_gate_time_list.append(n_block_change[i][0])
        n_gate_list.append(n_block_change[i][2][gate_name])
        n_gate_time_list.append(n_block_change[i+1][0])
        n_gate_list.append(n_block_change[i][2][gate_name])

    fig = plt.figure()
    ax = fig.add_subplot()
    lns1 = ax.plot(evolution_time_list, quality_list, '-',
                   color="dodgerblue", label="Distance")

    ax2 = ax.twinx()
    lns2 = ax2.plot(n_gate_time_list, n_gate_list, '-',
                    color="orange", label=gate_name+" count: Adaptive")
    lns3 = ax2.plot([0, end_time], [first_trotter_gate_use, first_trotter_gate_use],
                    '-', color="red", label=gate_name+" count: 1st Trotter ")
    ax.grid()
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance")
    ax2.set_ylabel("Number of gates")

    lns = lns2+lns1+lns3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper right', ncol=2)

    gate_used_lim = max(first_trotter_gate_use, n_gate_list[-1])

    ax2.set_ylim(0, gate_used_lim*1.3)
    ax.set_ylim(0, max(quality_list)*1.4)
    plt.savefig(path+'/run_status.png', bbox_inches='tight')


def generate_benchmark_for_compare_from_paths(paths, delta_n=1, trotter_steps=None, task_manager=None):
    if trotter_steps is None:
        trotter_steps = [1]
    label_list = []
    delta_t_list = []
    circuit_list_list = []
    for path in paths:
        circuit_list = read_circuits_from_file(path, delta_n=delta_n)
        circuit_list_list.append(circuit_list)
        with open(path + "/run_info.json", "r") as f:
            log_dict = json.load(f)
        label_list.append("D_cut "+str(log_dict["quality_cutoff"]))
        delta_t_list.append(log_dict["delta_t"])
    delta_t = max(delta_t_list)
    assert delta_t == min(delta_t_list)
    delta_t = delta_t*delta_n
    init_circuit = circuit_list_list[0][0]
    with open(paths[0] + "/energy_obj.pickle", "rb") as f:
        hamiltonian = pickle.load(f).hamiltonian

    for n_trotter_step in trotter_steps:
        list_n_circuit = [len(circuit_list)
                          for circuit_list in circuit_list_list]
        max_n_circuit = max(list_n_circuit)
        trotter_circuits = generate_trotter_benchmark_circuits(
            init_circuit, n_trotter_step, hamiltonian, delta_t, max_n_circuit)
        circuit_list_list.append(trotter_circuits)
        label_list.append("Trotter "+str(n_trotter_step))
    fidelity_list_list = generate_benchmark_for_compare(
        circuit_list_list, hamiltonian, delta_t, task_manager=task_manager)
    return fidelity_list_list, label_list, delta_t


def draw_benchmark_for_compare_from_paths(paths, delta_n=1, trotter_steps=None, task_manager=None):
    fidelity_list_list, label_list, delta_t = generate_benchmark_for_compare_from_paths(
        paths, delta_n=delta_n, trotter_steps=trotter_steps, task_manager=task_manager)
    min_fidelity = 1

    import matplotlib
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot()

    for i in range(len(fidelity_list_list)):
        fidelity_list = np.array(fidelity_list_list[i])
        x_data = [step*delta_t for step in range(len(fidelity_list))]
        ax.plot(x_data, (-1*fidelity_list)+1, '-o',
                label=label_list[i], alpha=0.8)
        local_min_fidelity = min(fidelity_list)
        if local_min_fidelity < min_fidelity:
            min_fidelity = local_min_fidelity

    ax.grid()
    ax.set_xlabel("Time")
    ax.set_ylabel("1-Fidelity")
    ax.legend(loc='upper right', ncol=3)
    max_diff = 1-min_fidelity
    ax.set_ylim(-max_diff*0.05, max_diff*1.2)

    for path in paths:
        plt.savefig(path+'/comprison.png', bbox_inches='tight')

def draw_n_gate_for_compare_from_paths(paths,stop_time=999999):

    import matplotlib
    import matplotlib.pyplot as plt
    #plt.style.use('ggplot')
    gate_name = "CNOT"
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.grid()
    ax.set_xlabel("Time")
    ax.set_ylabel(gate_name+" gate count")
    max_n_gate=0
    min_n_gate=999999
    for path in paths:
        with open(path + "/run_status_info.json", "r") as f:
            log_dict = json.load(f)
        with open(path + "/run_info.json", "r") as f:
            log_dict_0 = json.load(f)
        
        n_block_change = log_dict["n_block_change"]
        gate_name = "CNOT"
        n_gate_list = []
        n_gate_time_list = []
        for item in n_block_change:
            n_gate_time_list.append(item[0])
            n_gate_list.append(item[2][gate_name])
        end_time = log_dict["evolution_time_list"][-1]
        n_gate_list = []
        n_gate_time_list = []
        n_block_change.append((end_time, None, None))
        for i in range(len(n_block_change)-1):
            n_gate_time_list.append(n_block_change[i][0])
            n_gate_list.append(n_block_change[i][2][gate_name])
            next_time=n_block_change[i+1][0]
            if next_time>stop_time:
                n_gate_time_list.append(stop_time)
                n_gate_list.append(n_block_change[i][2][gate_name])
                break
            n_gate_time_list.append(n_block_change[i+1][0])
            n_gate_list.append(n_block_change[i][2][gate_name])
        max_n_gate=max(max_n_gate,max(n_gate_list))
        min_n_gate=min(min_n_gate,n_gate_list[0])
        ax.plot(n_gate_time_list, n_gate_list, '-', label="D_cut "+str(log_dict_0["quality_cutoff"]))
        
    ax.legend(loc='upper right', ncol=3)
    ax.set_ylim(min_n_gate*0.9,max_n_gate*1.2)

    for path in paths:
        plt.savefig(path+'/n_gate_for_compare.png', bbox_inches='tight')


def mkdir(path):
    is_dir_exists = os.path.exists(path)
    if not is_dir_exists:
        os.makedirs(path)
        return True
    else:
        return False


def get_hamiltoian_in_adiabatic(init_hamiltonian, final_hamiltonian, total_time, time_now):
    final_portion = time_now/total_time
    init_portion = 1-final_portion
    # print("portion",final_portion)
    new_hamiltonian = init_portion*init_hamiltonian+final_portion*final_hamiltonian
    return new_hamiltonian
