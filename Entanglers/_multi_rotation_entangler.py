from Entanglers._entangler import *


class RotationEntangler(Entangler):
    n_parameter = -1

    def __init__(self, rotation_entangler_list):
        self.rotation_entangler_list = rotation_entangler_list
