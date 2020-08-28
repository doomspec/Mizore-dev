from openfermion.ops import QubitOperator
from Utilities.Iterators import iter_partial_operators



hamiltonian=100*QubitOperator("")+QubitOperator("X1 X2")+0.5*QubitOperator("Z1 X2")+QubitOperator("Y1 X2")+QubitOperator("Y1 Z2")
for i in iter_partial_operators(hamiltonian,1):
    print(i)