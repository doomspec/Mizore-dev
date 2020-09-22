from ._time_evolution_contructor import TimeEvolutionConstructor, get_hamiltoian_in_adiabatic
from Blocks._utilities import get_circuit_energy
from Objective import EnergyObjective
from openfermion.ops import QubitOperator


class AdiabaticEvolutionConstructor(TimeEvolutionConstructor):
    
    def __init__(self, init_energy_obj, final_energy_obj, pool, init_circuit, **kwargs):
        self.init_hamiltonian = init_energy_obj.hamiltonian
        self.final_hamiltonian = final_energy_obj.hamiltonian
        self.init_energy_list=[]
        self.final_energy_list=[]
        energy_obj=EnergyObjective(1.01*self.init_hamiltonian+self.final_hamiltonian,init_energy_obj.n_qubit)
        TimeEvolutionConstructor.__init__(
            self,energy_obj, pool, init_circuit, **kwargs)
        
        pass

    def get_circuit_constructor(self):
        return self.get_circuit_constructor_by_hamiltonian(self.get_current_hamiltonian())

    def get_evolution_hamiltonian(self):
        return self.energy_obj.hamiltonian

    def get_current_hamiltonian(self):
        print(get_hamiltoian_in_adiabatic(self.init_hamiltonian, self.final_hamiltonian, self.total_time_to_evolve, self.total_time_evolved))
        return get_hamiltoian_in_adiabatic(self.init_hamiltonian, self.final_hamiltonian, self.total_time_to_evolve, self.total_time_evolved)

    def evolve(self, circuit, time):
        new_circuit, evolved_time=self.evolver.do_adiabatic_time_evolution(circuit, self.init_hamiltonian, self.final_hamiltonian,
                                                 time, final_time=self.total_time_to_evolve, start_time=self.total_time_evolved)
        init_energy=get_circuit_energy(new_circuit,self.init_hamiltonian)
        final_energy=get_circuit_energy(new_circuit,self.final_hamiltonian)
        self.init_energy_list.append(init_energy)
        self.final_energy_list.append(final_energy)
        print("Evolve finished")
        print("Final energy:",self.final_energy_list)
        return new_circuit,evolved_time

    def get_run_status_info_dict(self):
        log_dict = TimeEvolutionConstructor.get_run_status_info_dict(self)
        log_dict["init_energy_list"]=self.init_energy_list
        log_dict["final_energy_list"]=self.final_energy_list
        return log_dict


def get_init_hamil_by_HF_init(energy_obj):
    init_hamil=QubitOperator()
    for i in range(energy_obj.n_qubit):
        if i in energy_obj.init_block.qsubset:
            init_hamil+=QubitOperator("Z"+str(i))
        else:
            init_hamil-=QubitOperator("Z"+str(i))

    return EnergyObjective(init_hamil,energy_obj.n_qubit,init_block=energy_obj.init_block)