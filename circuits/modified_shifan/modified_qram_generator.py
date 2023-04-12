import sys
import random
"""
Modified (Dual-Rail) QRAM with n-address bits:
bus = 0
address = 1 ... n
input = n + 1

STEP 0: "Hadamard Transform" on input (0L = 01, 1L = 10)

STEP 1: LOADING THE TREE
Requires 2^n - 1 routers, each with 3 dual-rail qubits

STEP 2: APPLY X_i (at 2^n end positions, 2 in the 2^(n/2) leaf routers)

STEP 3: CNOT everything to bus in parallel (a "CNOT tree")

STEP 4: APPLY the entire circuit in reverse
"""

# number of address bits. 
n = int(sys.argv[1])

# offset for CNOT part (Step 3)
cnot_offset = 2 * (n + 1) + (6 * ((2 ** n) - 1))

# counter for cnot tree 
cnot_counter = 2 ** n

# makes a cswap operation dual rail. 
def dual_rail_cswap(x, y, z):
    return f"cswap {x} {y} {z} \ncswap {x} {y+1} {z+1} \n"

# make a swap operation dual rail. 
def dual_rail_swap(x, y):
    return f"swap {x} {y} \nswap {x+1} {y+1} \n"

# make a cnot operation dual rail. 
def dual_rail_cnot(x, y):
    return f"cx {x} {y}\ncx {x+1} {y+1} \n"


# maps a number k = b_1b_2...b_k to \sum 2^{i-1}b_i. 
# represents the position of the router in the qram tree, labeling the root 1, children 2, 3, etc.
# NOTE: qram routers are 0-indexed
def tree_position(k):
    return sum([(2 ** (i)) * ((k >> (n - i - 1)) % 2) for i in range(n)]) - 1

# tree structure of routers.
tree_layout = [tree_position(k) for k in range(1, 2 ** n)]

# get parent node, or None if it is the root
def parent(k):
    i = tree_layout.index(k)
    return None if i == 0 else i // 2

# get children, or None if it is a leaf
def children(k):
    i = tree_layout.index(k)
    return None if i >= len(tree_layout)/2 else (tree_layout[2 * i + 1], tree_layout[2 * i + 2])

# get first rail of the left qubit on a router
def left_qubit(k):
    if k == -1:
        return 2 * n
    return 2 * (n + 1) + (6 * k) 

# get first rail of the middle qubit on a router
def middle_qubit(k):
    if k == -1:
        return 2 * n
    return 2 * (n + 1) + (6 * k) + 2

# get first rail of the right qubit on a router
def right_qubit(k):
    if k == -1:
        return 2 * n
    return 2 * (n + 1) + (6 * k) + 4

# actually build the qram tree
def modified_qram():
    global n, cnot_counter, cnot_offset
    gates = ""
    cnot_queue = []
    # STEP 1
    for i in range(n):
        # swap next address qubit to input
        # gates += f"Swapping address {i} into input\n"
        gates += dual_rail_swap(2 * i, 2 * n)
        # load the root router
        if i == 0:
            # gates += "adding root\n"
            gates += dual_rail_swap(2 * n, middle_qubit(tree_layout[0]))
        else: 
            child_queue = [(-1, tree_layout[0], 0)]
            while len(child_queue) > 0:
                parent, current, depth = child_queue.pop(0)
                # print("POPPING OFF STACK", parent, current, depth)
                if depth < i:
                    # add cswap gadget, then add children
                    # gates += f"adding a cswap gadget at router {current}\n"
                    gates += dual_rail_cswap(middle_qubit(current), left_qubit(current), left_qubit(parent))
                    gates += dual_rail_cswap(middle_qubit(current) + 1, right_qubit(current), right_qubit(parent))
                    # add swap to child nodes
                    childs = children(current)
                    gates += dual_rail_swap(left_qubit(current), middle_qubit(childs[0]))
                    gates += dual_rail_swap(right_qubit(current), middle_qubit(childs[1]))
                    for child in childs:
                        child_queue.append((current, child, depth + 1))
                # add cnot/swap gadget at leaves (STEP 2)
                if depth == n - 1:
                    # gates += f"adding a cnot at leaf router {current}\n"
                    gates += f"cx {middle_qubit(current)} {left_qubit(current)}\n"
                    gates += f"cx {middle_qubit(current) + 1} {right_qubit(current)}\n"

                    # OLD gadget: not correct 
                    # gates += dual_rail_cnot(middle_qubit(current), right_qubit(current))
                    # gates += f"x {middle_qubit(current)}\n"
                    # gates += dual_rail_cnot(middle_qubit(current), left_qubit(current))
                    
                    # randomly add data
                    if random.random() < .5:
                        gates += f"swap {left_qubit(current)} {left_qubit(current) + 1}\n"
                    if random.random() < .5:
                        gates += f"swap {right_qubit(current)} {right_qubit(current) + 1}\n"
                    # STEP 3: outgoing CNOTs
                    # gates += f"adding initial outoing cnot at leaf router {current}\n"
                    target = cnot_offset + 2 * (tree_layout.index(current) - len(tree_layout) // 2)
                    gates += dual_rail_cnot(left_qubit(current), target)
                    gates += dual_rail_cnot(right_qubit(current), target)
                    cnot_queue.append((target, 2 * (cnot_counter // 2)))
                    cnot_counter -= 1
    
    # STEP 3 (con't):
    # gates += "adding the other cnot's\n"
    while len(cnot_queue) > 1:
        for elt in cnot_queue:
            gates += dual_rail_cnot(elt[0], elt[0] + elt[1])
        new_cnot_queue = []
        if cnot_counter > 1:
            for elt in cnot_queue[::2]:
                new_cnot_queue.append((elt[0] + elt[1], 2 * (cnot_counter // 2)))
                cnot_counter -= 1
        cnot_queue = new_cnot_queue
        # current, offset = cnot_queue.pop(0)
        # print("TAKEN OFF", current, offset)
        # if offset > 1:
            
        #     cnot_queue.append((current + 2 * (cnot_counter // 2), 2 * (cnot_counter // 2)))
        
    # STEP 4: Reverse list + return (except for bus)
    lst = gates.split("\n")[::-1][5:]

    # STEP 0: dual-rail hadamard transform 
    for i in range(n):  
        gates = f"x {2 * i + 1}\n" + gates
        gates = f"cx {2 * i} {2 * i + 1}\n" + gates
        gates = f"h {2 * i}\n" + gates

    # for step 3 later
    return f"{cnot_offset + ((2 ** n) * 2) - 2}\n#\n" + gates + "\n".join(lst)

with open(f"circuits/modified_shifan/size={n}", "w+") as f:
    f.write(modified_qram())