# Mizore

Mizore is an open source effort for quantum computing which focus on adaptive construction of the unitary that create the ground state of certain Hamiltonian.

## Setup
It is very simple to setup Mizore in your computer.

```shell
# clone mizore into your local computer
git clone https://github.com/doomspec/Mizore.git

# install mizore via setup.py
cd Mizore
python3 setup.py install
```

## First adptive-VQE program 

```python
from mizore.CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from mizore.HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian
from mizore.PoolGenerator import BlockPool,all_rotation_pool

# Generate the Hamiltonian
hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=bravyi_kitaev)

# Generate the exponentiated pauliword e^(iPt) block pool
pool=pool=BlockPool(all_rotation_pool(hamiltonian_obj.n_qubit,max_length=hamiltonian_obj.n_qubit))

# Generate the circuit constructor
constructor=GreedyConstructor(hamiltonian_obj,pool)

# Run the constructor
constructor.start()
constructor.join()
constructor.terminate()
```

## Authors
Zi-Jian Zhang, Jia-Qi Hu and Yi Liu from Southern University of Science and Technology (SUSTech, Shenzhen, China)

## The meaning of Mizore
Mizore is a Japanese word means sleet in English. Sleet contains both water and ice. Water is like parameter which can be adjusted continuously and ice is like blocks.
