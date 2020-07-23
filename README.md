# Mizore
![image](https://github.com/doomspec/Mizore/blob/master/mizore_icon.png)

Mizore is an open source effort for quantum computing which focus on adaptive construction of the quantum circuit for certain objective. Currently, Mizore focus on finding the quantum circuit that produce the ground state of a certain Hamiltonian by the Variational Quantum Eigensolver (VQE) approach. 

Mizore focus on providing a framework for adpative VQE described in [J. Chem. Theory Comput. 2020, 16, 2](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01084) and [Nat Commun 10, 3007 (2019)](https://www.nature.com/articles/s41467-019-10988-2), where the structure of the parameterized circuit can be optimized, differing from traditional VQE which uses a fixed parameterized circuit and only adjusts the parameter.

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
