import itertools

def is_contain_odd_Y(pauli):
    y_num = 0
    for i in pauli:
        if i == 2:
            y_num += 1
    is_valid= (y_num % 2 == 1)
    return is_valid

def iter_odd_Y_pauli(length):
    for pauli in itertools.product(range(1, 4), repeat=length):
        if not is_contain_odd_Y(pauli):
            continue
        yield pauli

def iter_qsubset(length, indices):
    for qs in itertools.combinations(range(0, len(indices)), length):
        qsubset = []
        for i in qs:
            qsubset.append(indices[i])
        yield qsubset

def iter_qsubset_odd_Y_pauli_by_length(length, indices):
    for qsubset in iter_qsubset(length,indices):
        for pauli in iter_odd_Y_pauli(length):
            yield qsubset,pauli

def iter_qsubset_odd_Y_pauli(indices):
    for length in range(len(indices)):
        for qsubset,pauli in iter_qsubset_odd_Y_pauli_by_length(length+1,indices):
            yield qsubset,pauli

def iter_all_qsubset_pauli_by_length(length, indices):
    for qsubset in iter_qsubset(length,indices):
        for pauli in itertools.product(range(1, 4), repeat=length):
            yield qsubset,pauli