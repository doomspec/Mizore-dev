from CircuitConstructor import GreedyConstructor
from openfermion.transforms import bravyi_kitaev
from HamiltonianGenerator import get_example_molecular_hamiltonian
from PoolGenerator import BlockPool,quasi_imaginary_evolution_rotation_pool

if __name__=="__main__":
    
    """
    Implementation of the paper
    "Short-depth trial-wavefunctions for the variational quantum eigensolver 
    based on the problem Hamiltonian"
    arXiv:1908.09533v1
    """

    # Generate the Hamiltonian
    hamiltonian_obj=get_example_molecular_hamiltonian("H2",basis="6-31g",fermi_qubit_transform=bravyi_kitaev)

    # Generate the block pool
    pool=BlockPool(quasi_imaginary_evolution_rotation_pool(hamiltonian_obj.hamiltonian))

    # Generate the circuit constructor
    constructor=GreedyConstructor(hamiltonian_obj,pool)

    # Run the constructor
    constructor.start()
    constructor.join()
    
    constructor.terminate()

"""
Here is GreedyConstructor
Size of Block Pool: 148
Initial Energy: -1.1267553171969316
Block added, energy now is: -1.1330348090231128 Hartree
Distance to target energy: 0.017637735938125454
Block Num:2; Qubit Num:8
Block list:
Type:HartreeFockInitBlock; Para Num:0; Qsubset:[0]
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 6]; Pauli:YZX
Doing global optimization
Global Optimized Energy: -1.1330348090231128
Block added, energy now is: -1.138459512743976 Hartree
Distance to target energy: 0.01221303221726222
Block Num:3; Qubit Num:8
Block list:
Type:HartreeFockInitBlock; Para Num:0; Qsubset:[0]
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 6]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 4]; Pauli:YZX
Doing global optimization
Global Optimized Energy: -1.1384798796731028
Block added, energy now is: -1.1432912609300145 Hartree
Distance to target energy: 0.007381284031223734
Block Num:4; Qubit Num:8
Block list:
Type:HartreeFockInitBlock; Para Num:0; Qsubset:[0]
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 6]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 4]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 2, 3]; Pauli:XZYZ
Doing global optimization
Global Optimized Energy: -1.1433067403016866
Block added, energy now is: -1.1474088328135126 Hartree
Distance to target energy: 0.0032637121477256947
Block Num:5; Qubit Num:8
Block list:
Type:HartreeFockInitBlock; Para Num:0; Qsubset:[0]
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 6]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 4]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 2, 3]; Pauli:XZYZ
Type:RotationEntangler; Para Num:1; Qsubset:[0, 2, 3, 5, 6]; Pauli:XZYZX
Doing global optimization
Global Optimized Energy: -1.1474467744036596
Block added, energy now is: -1.1513833036952659 Hartree
Distance to target energy: -0.0007107587340275945
Block Num:6; Qubit Num:8
Block list:
Type:HartreeFockInitBlock; Para Num:0; Qsubset:[0]
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 6]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 4]; Pauli:YZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 1, 2, 3]; Pauli:XZYZ
Type:RotationEntangler; Para Num:1; Qsubset:[0, 2, 3, 5, 6]; Pauli:XZYZX
Type:RotationEntangler; Para Num:1; Qsubset:[0, 2, 3, 5, 6]; Pauli:XXYZZ
Doing global optimization
Global Optimized Energy: -1.1514262336849594
Target energy achieved by 6  blocks!
Construction process ends!
"""