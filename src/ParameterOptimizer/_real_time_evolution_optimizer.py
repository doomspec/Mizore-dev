from ._imaginary_time_evolution_optimizer import ImaginaryTimeEvolutionOptimizer
from scipy import linalg
import numpy
from Utilities.Tools import random_list


class RealTimeEvolutionOptimizer(ImaginaryTimeEvolutionOptimizer):
    def __init__(self, *args, **kwargs):
        ImaginaryTimeEvolutionOptimizer.__init__(self, *args, **kwargs)

    def calc_A_mat(self, circuit, adjusted_circuits):
        return numpy.imag(self.calc_complex_A_mat(circuit, adjusted_circuits))
