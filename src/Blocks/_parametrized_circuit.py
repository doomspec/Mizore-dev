class ParametrizedCircuit:
    def __init__(self, ansatz, n_qubit, n_parameter):
        self.ansatz = ansatz
        self.n_qubit = n_qubit
        self.n_parameter = n_parameter
