import os,pickle

RESULT_PATH="mizore_results/"
CIRCUIT_PATH=RESULT_PATH+"block_circuits/"

def mkdir(path):
    is_dir_exists = os.path.exists(path)
    if not is_dir_exists:
        os.makedirs(path)
        return True
    else:
        return False

def save_circuit(circuit,circuit_name):
    mkdir(CIRCUIT_PATH)
    path=CIRCUIT_PATH+circuit_name+".bc"
    with open(path, "wb") as f:
        pickle.dump(circuit, f)