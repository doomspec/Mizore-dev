from .Iterators import iter_qsubset_pauli_of_operator
from openfermion.ops import QubitOperator

number2pauli_name = ["I", "X", "Y", "Z"]


def random_list(start, stop, length):
    """
    This function generates a array of random float numbers with certain length 
    The numbers are randomly chosen from start to stop
    """
    import random
    if length >= 0:
        length = int(length)
    start, stop = (start, stop) if start <= stop else (stop, start)
    random_list = []
    for i in range(length):
        random_list.append(random.uniform(start, stop))
    return random_list


def get_operator_chain(operator: QubitOperator):
    qubit_set = [False] * 200  # Assume there are at most 200 qubits
    for qsubset, pauli in iter_qsubset_pauli_of_operator(operator):
        for i in qsubset:
            qubit_set[i] = True
    qsubset = []
    for i in range(len(qubit_set)):
        if qubit_set[i]:
            qsubset.append(i)
    return qsubset


def pauliword2string(pauli):
    string = ""
    for i in pauli:
        string += number2pauli_name[i]
    return string


if __name__ == "__main__":
    print(get_operator_chain(QubitOperator("X0 X2")))
