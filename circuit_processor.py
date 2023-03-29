import random
import os
from query_fidelity import queryFidelity as qf
import numpy as np
import sys
import string

"""
Read in a BB circuit, add some Z noise, then generate data
"""
n = int(sys.argv[1])
SHOTS = 5000
exp = 5 # error prob is 10^{-exp}

fidelities = []
with open(f"circuits/bucket_brigade_circuits/size={n}") as bb:
    # obtain the data for the good simulator
    os.system(f"./fp.out bucket_brigade_circuits/size={n} -d bb{n}")
    correct_circuit = bb.readlines()
    # get the data of the correct circuit
    expected = dict()
    with open(f"data/bb{n}") as res:
        for line in res.readlines():
            ket, real, imag = line.replace("(", "").strip(")\(\n").split(",")
            expected[int(ket)] = float(real) + 1j * float(imag)

    # number of error shots
    for x in range(SHOTS):
        # load error circuit
        error_circuit = []
        for gate in correct_circuit:
            tokens = gate.split()
            error_circuit.append(gate)
            for i in range(1, len(tokens)):
                # NOTE THE ERROR: z error, 1/1000 probability
                ra = random.random()
                prob = 10 ** -exp
                if int(tokens[i]) > n:
                    if ra < prob / 3:
                        error_circuit.append(f"x {tokens[i]}\n")
                    elif ra < 2 * prob / 3:
                        error_circuit.append(f"y {tokens[i]}\n")
                    elif ra < prob:
                        error_circuit.append(f"z {tokens[i]}\n")
                    
        
        # write the data of the error simulated circuit
        random_name = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=32))
        with open(f"circuits/bucket_brigade_circuits/bbtemp{random_name}.txt", "w") as error_file:
            for gate in error_circuit:
                error_file.write(gate)
        os.system(f"./fp.out bucket_brigade_circuits/bbtemp{random_name}.txt -d bb{random_name}error")
        os.remove(f"circuits/bucket_brigade_circuits/bbtemp{random_name}.txt")

        # get the data of the error circuit
        observed = dict()
        with open(f"data/bb{random_name}error") as res:
            for line in res.readlines():
                ket, real, imag = line.replace("(", "").strip(")\(\n").split(",")
                observed[int(ket)] = float(real) + 1j * float(imag)
        os.remove(f"data/bb{random_name}error")


        # compute the query fidelity for this shot 
        fidelity = qf(n, observed, expected)
        fidelities.append(fidelity)
        print(f"bb{n}, shot{x}. fidelity=", fidelity)

with open("results.txt", "a+") as f:
    f.write(f"Experiment: BB{n}, Depolarizing error prob = 10^-{exp}. # of monte carlo samples: {SHOTS}. Mean Fidelity: {np.mean(fidelities)}. Std Dev:{np.std(fidelities)}\n" )

"""


Read in all of shifan's circuits
"""

