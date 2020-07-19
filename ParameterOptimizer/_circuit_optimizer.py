from Entanglers._entangler_circuit import EntanglerCircuit
from scipy.optimize import minimize, basinhopping
from ParameterOptimizer.ObjWrapper import get_obj_for_optimizer
from Utilities.Tools import random_list
from Entanglers._parametrized_circuit import ParametrizedCircuit

def basinhopping_optimizer(pcircuit:ParametrizedCircuit, hamiltonian, random_initial=0, niter=10, temperature=0.5):

    initial_parameter=[0.0]*pcircuit.n_parameter
    

    if random_initial != 0:
        initial_parameter = random_list(-random_initial, random_initial, pcircuit.n_parameter
    )

    obj=get_obj_for_optimizer(pcircuit,hamiltonian)

    opt_result = basinhopping(obj, initial_parameter, niter=niter,
                              T=temperature, stepsize=1e-6, minimizer_kwargs={"tol": 1e-4, "method": 'BFGS'},
                              take_step=None, accept_test=None, callback=None,
                              disp=False, niter_success=None)

    return opt_result.fun, opt_result.x
