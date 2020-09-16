from CircuitConstructor._no_parameter_constructor import NoParameterConstructor
from Objective._vqs_quality_obj import CircuitQualityObjective
from ParameterOptimizer import RealTimeEvolutionOptimizer

class TimeEvolutionConstructor():

    def __init__(self,energy_obj,pool,init_circuit,quality_cutoff=0.0001,diff=1e-4,n_step=3,n_circuit=3,stepsize=1e-3,n_block_per_step=1):
        self.energy_obj=energy_obj
        self.circuit=init_circuit
        self.quality_cutoff=quality_cutoff
        self.pool=pool
        self.diff=diff
        self.quality_obj=CircuitQualityObjective(energy_obj,self.diff)
        self.n_step=n_step
        self.n_circuit=n_circuit
        self.stepsize=stepsize
        self.evolver=RealTimeEvolutionOptimizer(random_adjust=0.0,
                                            verbose=True, n_step=self.n_step,quality_cutoff=self.quality_cutoff,stepsize=self.stepsize,diff=self.diff, max_increase_n_step=self.n_step,
                                            calculate_quality=True, inverse_evolution=False)

        pass

    def run(self):
        step_evolved=0
        circuit_list=[self.circuit.duplicate()]
        construct_needed=False
        while(True):
            if construct_needed:
                constructor=NoParameterConstructor(self.quality_obj,self.pool,terminate_cost=self.quality_cutoff,init_circuit=self.circuit)
                new_circuit=constructor.run()
                new_circuit.set_all_block_active()
            else:
                new_circuit=self.circuit
            local_n_step=self.n_step-step_evolved%self.n_step
            new_circuit,quality_list=self.evolver.run_optimization(new_circuit,self.energy_obj.hamiltonian,local_n_step)
            step_evolved+=len(quality_list)
            construct_needed = (local_n_step!=len(quality_list))
            if step_evolved%self.n_step==0:
                circuit_list.append(new_circuit.duplicate())
            print("n_step_evolved",step_evolved,"Quality:",quality_list)
            self.circuit=new_circuit
            if len(circuit_list)==self.n_circuit+1:
                return circuit_list
            