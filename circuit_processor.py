import random
import os
from query_fidelity import queryFidelity as qf
import numpy as np
import sys
import string
import time
"""
Read in a BB circuit, add some Z noise, then generate data
"""
n = int(sys.argv[1])
SHOTS = int(sys.argv[2])
exp = int(sys.argv[3]) # error prob is 10^{-exp}
error_type = sys.argv[4]
error_gate = sys.argv[5]
fidelities = []
name = sys.argv[6]

## BB EXPERIMENTS ## 
if name == "bb":
    start = time.time()
    with open(f"circuits/bucket_brigade_circuits/size={n}") as bb:
        # obtain the data for the good simulator
        # os.system(f"./fp.out bucket_brigade_circuits/size={n} -d bb{n}")
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
                    ra = random.random()
                    prob = 10 ** -exp
                    if int(tokens[i]) > n: # n is specific to BB architecture 
                        if ra < prob:
                            error_circuit.append(f"{error_gate} {tokens[i]}\n")
                        
            
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
            with open(f"data/bb{random_name}error", "r+") as res:
                for line in res.readlines():
                    ket, real, imag = line.replace("(", "").strip(")\(\n").split(",")
                    observed[int(ket)] = float(real) + 1j * float(imag)
            os.remove(f"data/bb{random_name}error")


            # compute the query fidelity for this shot 
            fidelity = qf(observed, expected)
            fidelities.append(fidelity)
            print(f"bb{n}, shot{x}. fidelity=", fidelity)
    
    end = time.time()

    # write the summary data
    with open("output/results.txt", "a") as f:
        f.write(f"bb{n}, {error_type}, {10 ** -exp}, {SHOTS}, {np.mean(fidelities)}, {np.std(fidelities)}, {end-start}\n" )

    # write the calculated fidelity for each shot
    with open(f"output/bb{n}_error={error_type}:10^-{exp}.txt", "w+") as f:
        for fidelity in fidelities:
            f.write(str(fidelity) + "\n")
    

## MODIFIED QRAM EXPERIMENTS
elif name == "modified":
    start = time.time()
    with open(f"circuits/modified/size={n}") as circ:
        # obtain the data for the good simulator
        # os.system(f"./fp.out modified/size={n} -d modified{n}")
        correct_circuit = circ.readlines()
        # get the data of the correct circuit
        expected = dict()
        with open(f"data/modified{n}") as res:
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
                
                    ra = random.random()
                    prob = 10 ** -exp
                    if int(tokens[i]) > 2 * n: # 2 * n is specific to modifiedz architecture 
                        if ra < prob:
                            error_circuit.append(f"{error_gate} {tokens[i]}\n")
                        
            
            # write the data of the error simulated circuit
            random_name = ''.join(random.choices(string.ascii_uppercase, k=32))
            with open(f"circuits/modified/temp{random_name}.txt", "w") as error_file:
                for gate in error_circuit:
                    error_file.write(gate)
            
            os.system(f"./fp.out modified/temp{random_name}.txt -d modified{random_name}error")
            os.remove(f"circuits/modified/temp{random_name}.txt")

            # get the data of the error circuit
            observed = dict()
            with open(f"data/modified{random_name}error", "r+") as res:
                for line in res.readlines():
                    ket, real, imag = line.replace("(", "").strip(")\(\n").split(",")
                    observed[int(ket)] = float(real) + 1j * float(imag)
            os.remove(f"data/modified{random_name}error")


            # compute the query fidelity for this shot 
            fidelity = qf(observed, expected)
            fidelities.append(fidelity)
            print(f"modified{n}, shot{x}. fidelity=", fidelity)
    end = time.time()

    # write the summary data
    with open("output/results.txt", "a") as f:
        f.write(f"modified{n}, {error_type}, {10 ** -exp}, {SHOTS}, {np.mean(fidelities)}, {np.std(fidelities)}, {end-start}\n" )

    # write the calculated fidelity for each shot
    with open(f"output/shifan_circuit_data{n}_error={error_type}:10^-{exp}.txt", "w+") as f:
        for fidelity in fidelities:
            f.write(str(fidelity) + "\n")

else:
    print("name not recognized")
    exit(1)