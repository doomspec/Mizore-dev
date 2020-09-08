from projectq.backends import Simulator
import time

sim = Simulator()
ind = 1
begin = time.time()
for i in range(40):
    sim.allocate_qubit(i)
    print(f'{ind}, {time.time() - begin}')
    ind += 1