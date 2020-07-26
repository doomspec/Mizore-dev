# Mizore
<img src="docs/mizore_icon.png" width="30%" align="left" />

Mizore is an open source effort for quantum computing which focus on adaptive construction of the quantum circuit for certain objective. Currently, Mizore focus on finding the quantum circuit that produce the ground state of a certain Hamiltonian by the Variational Quantum Eigensolver (VQE) approach. 

Mizore focus on providing a framework for adpative VQE similar to what is described in [J. Chem. Theory Comput. 2020, 16, 2](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01084) and [Nat Commun 10, 3007 (2019)](https://www.nature.com/articles/s41467-019-10988-2), where the structure of the parameterized circuit can be optimized, differing from traditional VQE which uses a fixed parameterized circuit and only adjusts the parameter. While providing better perfermance of convergence, adaptive method can also achieve certain objective with fewer quantum gates. We believe that adaptive circuit construction is a key method for near-term quantum applications.

## Setup
It is very simple to setup Mizore in your computer.

```shell
# clone mizore into your local computer
git clone https://github.com/doomspec/Mizore.git

# install mizore via setup.py
cd Mizore
sudo python3 setup.py install
```

## First adptive-VQE program 

```python
from mizore.CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from mizore.HamiltonianGenerator.TestHamiltonian import get_example_molecular_hamiltonian
from mizore.PoolGenerator import BlockPool,all_rotation_pool

# Generate the Hamiltonian
hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="sto-3g",fermi_qubit_transform=bravyi_kitaev)

# Generate the high-dimensional rotation e^(iPt) block pool
pool=BlockPool(all_rotation_pool(hamiltonian_obj.n_qubit,max_length=hamiltonian_obj.n_qubit))

# Generate the circuit constructor
constructor=GreedyConstructor(hamiltonian_obj,pool)

# Run the constructor
constructor.start()
constructor.join()
constructor.terminate()
```
## Key ideas
Differing from using elementary gate set from circuit construction, we introduce the concept *block* (mizore.Blocks.Block). A block is a piece of parameterized circuit that implements certain unitary such as a double excitation and high-dimensional rotation. In a run of Mizore program, one first generate a elementary block set for the construction which we call *block pool* (mizore.PoolGenerator.BlockPool). Then, one use certain circuit constructor (in mizore.CircuitConstructor) to find a block circuit (mizore.Blocks.BlockCircuit) that achieves certain objective (mizore.Objective) using the blocks in the block pool. For detail usage instruction of these modules, please refer to the annotation in the sourse codes. 

<img src="docs/mizore_lifetime.png" width="90%" align="center" />

Also, we provide methods for conveniently construct the problem Hamiltonian for tests in mizore.HamiltonianGenerator using PySCF and openfermion (HiQ Fermion). Parallel run of circuit evaluation is implemented in mizore.ParallelTaskRunner. Optimization methods including basin-hopping and ansatz-based imaginary time evolution ([npj Quantum Information (2019) 5:75](https://www.nature.com/articles/s41534-019-0187-2)) is implemented in mizore.ParameterOptimizer. The simulation of quantum circuit is implemented by Huawei's fork of ProjectQ (HiQ Simulator).

We implement several adpative VQE methods presented in previous works in mizore.Example using the Mizore framework.

## Plans and Future
We plan to 
1. Implement modules for visulization of Mizore runs
2. Harness machine learning methods for block arrangement
3. Implement modules to use adaptive circuit construction for more objectives such as producing excited states
   

## Authors
Zi-Jian Zhang (张子健), Jia-Qi Hu (胡家祺) and Yi Liu (刘艺) from Southern University of Science and Technology (SUSTech, Shenzhen, China)

## The meaning of Mizore
霙 is a east-asian word reads *mizore* in Japanese and *ying* in Chinese. Mizore means sleet in English. The parameters in the circuit is like water because they can be adjusted continuously and the blocks in the circuit is like ice because they have fixed shape. In adaptive circuit construction, the blocks and parameters in the circuit are both optimized. Therefore, it is like sleet which contains both water and ice.
