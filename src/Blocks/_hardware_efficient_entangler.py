from Blocks import Block
from Utilities.Operations import full_rotation,inversed_full_rotation,CNOT_entangler,inversed_CNOT_entangler

class HardwareEfficientEntangler(Block):
    
    IS_INVERSE_DEFINED = True

    def __init__(self, qsubset, init_angle=None):
        Block.__init__(self, n_parameter=3*len(qsubset),active_qubits=qsubset)
        if init_angle==None:
            init_angle=[0.0]*self.n_parameter
        self.parameter = init_angle
        self.qsubset = qsubset

    def apply_forward_gate(self, parameter, wavefunction):
        full_rotation(wavefunction,self.qsubset,[self.parameter[i]+parameter[i] for i in range(len(self.parameter))])
        CNOT_entangler(wavefunction,self.qsubset)
        return

    def apply_inverse_gate(self, parameter, wavefunction):
        inversed_CNOT_entangler(wavefunction,self.qsubset)
        inversed_full_rotation(wavefunction,self.qsubset,[self.parameter[i]+parameter[i] for i in range(len(self.parameter))])
        return

    def get_gate_used(self):
        return {"CNOT":len(self.qsubset),"SingleRotation":len(self.qsubset)}

    def __str__(self):
        info = self.basic_info_string()
        info += "; Qsubset:" + str(self.qsubset)
        return info

