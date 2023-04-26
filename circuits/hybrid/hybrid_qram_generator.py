import sys

sys.path.append('../modified')

from modified_qram_generator import modified_qram as mod
from modified_qram_generator import dual_rail_cswap


# n qubit address space, first k are QROM (so there are 2^{n-k} copies of the QRAM)
def hybrid(n, k):
    assert n - k == int(sys.argv[1])
    output = ""

    if k > 2:
        return "This is not supported."
    qram = mod(n - k).split("\n")
    qram_init = qram[2: 3 * int(sys.argv[1]) + 2] 
    a = qram[3 * int(sys.argv[1]) + 2: ] 

    output += str(int(qram[0]) + 2 * n) + "\n#\n"
    for line in qram_init:
        output += line + "\n"
    for i in range(2 ** k):
        # add the qrom x gates
        for j in range(k):
            if (i >> j + 1) % 2 == 0:
                output += f"x {2 * j}\n"
                output += f"x {2 * j + 1}\n"
        # add the qrom cnots/ccnots
        if k == 1:
            output += f"cx {0} {2 * n}\n"
            output += f"cx {1} {2 * n + 1}\n"
        elif k == 2:
            output += f"ccx {0} {1} {2 * n}\n"
            output += f"ccx {1} {3} {2 * n + 1}\n"
        # add the swaps
        for i in range(2 * k, 2 * n, 2):
            output += dual_rail_cswap(2 * n, i, 2 * (n - k + 1 + i // 2))

        # new_a is the shifted qram
        new_a = []
        for x in a:
            shifted_x = []
            for token in x.strip(" ").split(" "):
                try:
                    shifted_x.append(str(int(token) + 2 * (n)))
                except: 
                    shifted_x.append(token)
            shifted_x = " ".join(shifted_x)
            new_a += shifted_x + "\n"
        new_a = "".join(new_a)
        output += new_a 

       
        # add the qrom cnots/ccnots
        if k == 1:
            output += f"cx {0} {2 * n}\n"
            output += f"cx {1} {2 * n + 1}\n"
        elif k == 2:
            output += f"ccx {0} {1} {2 * n}\n"
            output += f"ccx {1} {3} {2 * n + 1}\n"
        # add the qrom x gates
        for j in range(k):
            if (i >> j + 1) % 2 == 0:
                output += f"x {2 * j}\n"
                output += f"x {2 * j + 1}\n"
        # add the swaps
        for i in range(2 * k, 2 * n, 2):
            output += dual_rail_cswap(2 * n, i, 2 * (n - k + 1 + i // 2))
    return output

with open("circuits/hybrid/size=(4,2).txt", "w") as f:
    for line in hybrid(4, 2):
        f.write(line)
