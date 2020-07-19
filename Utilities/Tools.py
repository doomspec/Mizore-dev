number2pauli_name=["I","X","Y","Z"]

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

def pauliword2string(pauli):
    string=""
    for i in pauli:
        string+=number2pauli_name[i]
    return string

if __name__=="__main__":
    print(pauliword2string([1,2,3]))