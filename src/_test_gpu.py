from Blocks import BlockCircuit, HardwareEfficientEntangler
from Utilities.CircuitEvaluation import evaluate_ansatz_1DMs
from Utilities.Tools import random_list
import time

n_qubit = 16
bc = BlockCircuit(16)

n_layer = 3
for i in range(n_layer):
    bc.add_block(HardwareEfficientEntangler(list(range(n_qubit))))
pcircuit = bc.get_ansatz_on_active_position()
n_para = pcircuit.n_parameter

n_iter = 100
start_time = time.time()

for i in range(n_iter):
    evaluate_ansatz_1DMs(random_list(-1, 1, n_para), pcircuit.n_qubit, pcircuit.ansatz)

# pcircuit.ansatz(random_list(-1,1,n_para),wavefunction)

time_each = (time.time() - start_time) / n_iter
print("Time used for each run:", time_each)
