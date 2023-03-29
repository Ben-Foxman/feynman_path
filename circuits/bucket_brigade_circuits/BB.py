from audioop import add
import math
from qiskit import *
from RouterTree import RouterTree
import numpy as np
from random import randint


class BucketBrigade(object):
    """
    Implementation of the Bucket Brigade QRAM Circuit as described in https://arxiv.org/abs/2012.05340

    Parameters:
    addr_size: A positive integer n speciying the number of address qubits for the circuit
    data: a number from 0 to 2^addr_size - 1 inclusive specifying the data stored by the circuit
    name (optional): name of the circuit
    """

    def __init__(self, addr_size: np.int64, data=0, name="BB") -> None:
        assert addr_size > 0
        assert 0 <= data < 2 ** (2 ** addr_size)
        self.name = name
        self.addr_size = addr_size

        self.bus = QuantumRegister(1, "bus")
        self.address = QuantumRegister(addr_size, "address")
        self.ancilla = QuantumRegister(1, "input (ancilla)")


        # internal routing numbers uses 0 for the root, 1/2 for left right child, 3/4/5/6 for second layer, etc.
        self.routing_tree = RouterTree(addr_size)
        self.routers = [x for x in self.routing_tree.array]

        self.circuit = QuantumCircuit(
            self.bus, self.address, self.ancilla, *[x.register for x in self.routers]
        )



        # load the addresses into the circuit
        for i in range(addr_size):
            self.addressToInput(i)
            self.routeLayer(i)
            self.swapLayer(i)

        # swap bus onto ancilla
        self.circuit.swap(self.bus[0], self.ancilla[0])
        # routing the bus to the appropriate memory cell uses the same routing structure
        self.routeLayer(addr_size + 1)

        # route in done, data copying layer
        inv = self.circuit.inverse()
        d = data
        for i in range(np.power(2, addr_size - 1) - 1, np.power(2, addr_size) - 1):
            for j in [0, 2]:
                b = d & 1
                d >>= 1
                if b == 1:
                    for router in self.routers:
                        if router.number == i:
                            self.circuit.x(router.register[j])

        # modify the qubits
        qr = QuantumRegister(self.circuit.num_qubits)
        self.finalCircuit = QuantumCircuit(qr, name=name)
        self.finalCircuit.append(
            self.circuit,
            [qr[x] for x in range(self.circuit.num_qubits)],
        )
        self.finalCircuit.append(
            inv,
            [qr[x] for x in range(self.circuit.num_qubits)],
        )

        # route out done
        self.finalCircuit = self.finalCircuit.decompose()

        self.finalCircuit = self.finalCircuit.inverse()
        # uniform superposition input
        for i in range(1, addr_size + 1):
            self.finalCircuit.h(i)
        self.finalCircuit = self.finalCircuit.inverse()

        self.circuit = self.finalCircuit

    # get the circuit
    def getCircuit(self):
        return self.circuit

    def addressToInput(self, level: int):
        self.circuit.swap(self.address[self.addr_size - level - 1], self.ancilla[0])

    def routeLayer(self, level: int):
        for i in range(1, level + 1):
            if i == 1:
                self.addRouting(self.routing_tree.root, self.ancilla[0])
            else:
                for router in self.routers:
                    if (2 ** (i - 1)) - 1 <= router.number < (2 ** i) - 1:
                        target = 0
                        if (router.parent.number + 1) * 2 == router.number:
                            target = 2

                        self.addRouting(router, router.parent.register[target])

    def swapLayer(self, level: int):
        # set top node of the tree
        if level == 0:
            self.circuit.swap(self.ancilla[0], self.routing_tree.root.register[1])
        else:
            # add swaps for later levels
            for router in self.routers:
                if (2 ** level) - 1 <= router.number < (2 ** (level + 1)) - 1:
                    target = 0
                    if (router.parent.number + 1) * 2 == router.number:
                        target = 2

                    self.circuit.swap(
                        router.register[1], router.parent.register[target]
                    )

    # subroutine to add left and right routing for a given router
    def addRouting(self, router, target: QuantumRegister):
        self.circuit.cswap(router.register[1], router.register[2], target)
        self.circuit.x(router.register[1])
        self.circuit.cswap(router.register[1], router.register[0], target)
        self.circuit.x(router.register[1])

    def _swap_qubit(self, router_number: int) -> QuantumRegister:
        # top node
        if router_number == (2 ** (self.addr_size - 1)) - 1:
            return self.ancilla

    def draw(self) -> None:
        self.finalCircuit.draw(output="mpl", filename=f"./{self.name}.png")


 
for i in range(1, 11):
    name = f"size={i}"
    with open(name, "w") as f:
        x = BucketBrigade(i, data=randint(0, 2 ** (2 ** i) - 1))
        f.write(str(x.getCircuit().num_qubits) + "\n")
        f.write("#\n")
        for g in x.getCircuit():
            f.write(g[0].name + " " + " ".join([str(a.index) for a in g[1]]) + "\n")


