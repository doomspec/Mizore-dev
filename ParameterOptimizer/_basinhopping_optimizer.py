from scipy.optimize import minimize, basinhopping
from ParameterOptimizer.ObjWrapper import get_obj_for_optimizer
from Utilities.Tools import random_list
from ParameterOptimizer import ParameterOptimizer


class BasinhoppingOptimizer(ParameterOptimizer):

    def __init__(self, random_initial=0.01, niter=10, temperature=0.5, stepsize=1e-6, tol=1e-6):
        ParameterOptimizer.__init__(self)

        self.random_initial = random_initial
        self.niter = niter
        self.temperature = temperature
        self.stepsize = stepsize
        self.tol = tol

    def run_optimization(self, circuit, hamiltonian):
        pcircuit = circuit.get_ansatz_on_active_position()

        initial_parameter = [0.0] * pcircuit.n_parameter

        if self.random_initial != 0:
            initial_parameter = random_list(-self.random_initial, self.random_initial, pcircuit.n_parameter
                                            )

        obj = get_obj_for_optimizer(pcircuit, hamiltonian)

        opt_result = basinhopping(obj, initial_parameter, niter=self.niter,
                                  T=self.temperature, stepsize=self.stepsize, minimizer_kwargs={
                "tol": self.tol, "method": 'BFGS'},
                                  take_step=None, accept_test=None, callback=None,
                                  disp=False, niter_success=None)

        return opt_result.fun, opt_result.x
