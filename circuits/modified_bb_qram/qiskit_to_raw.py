#!/usr/bin/env python
# coding: utf-8

import numpy as np

# Import Qiskit
from qiskit import *


# r11 is layer 1 router, r21is layer two router corresponds to left branch, similar for r22.

bus = QuantumRegister(2, name="bus")
add = QuantumRegister(4, name="address")
inp = QuantumRegister(2, name="input")
r22 = QuantumRegister(6, name="router2.2")
r21 = QuantumRegister(6, name="router2.1")
r11 = QuantumRegister(6, name="router1.1")
qreg_data = QuantumRegister(4, name="data")


# swap address in u1
qc = QuantumCircuit(bus, add, inp, r22, r11, r21, qreg_data)
qc.swap(add[3], inp[1])
qc.swap(add[2], inp[0])
qc.swap(inp[0], r11[2])
qc.swap(inp[1], r11[3])

qc.swap(add[1], inp[1])
qc.swap(add[0], inp[0])
qc.cswap(r11[3], inp[1], r11[5])
qc.cswap(r11[3], inp[0], r11[4])
qc.cswap(r11[2], inp[1], r11[1])
qc.cswap(r11[2], inp[0], r11[0])

qc.swap(r22[2], r11[0])
qc.swap(r22[3], r11[1])
qc.swap(r21[2], r11[4])
qc.swap(r21[3], r11[5])

# create initial data register state u2
qc.cnot(r21[2], r21[1])
qc.cnot(r21[3], r21[5])
qc.cnot(r22[2], r22[1])
qc.cnot(r22[3], r22[5])

# classical controlled-swap u3
qc.cswap(qreg_data[0], r21[4], r21[5])
qc.cswap(qreg_data[1], r21[0], r21[1])
qc.cswap(qreg_data[2], r22[4], r22[5])
qc.cswap(qreg_data[3], r22[0], r22[1])

# data retieving u4
qc.cnot(r21[4], r11[4])
qc.cnot(r21[5], r11[5])
qc.cnot(r21[0], r11[4])
qc.cnot(r21[1], r11[5])


qc.cnot(r22[4], r11[0])
qc.cnot(r22[5], r11[1])
qc.cnot(r22[0], r11[0])
qc.cnot(r22[1], r11[1])

qc.cnot(r11[4], bus[0])
qc.cnot(r11[5], bus[1])
qc.cnot(r11[0], bus[0])
qc.cnot(r11[1], bus[1])

# data retieving u4+(notice different from u4)
qc.cnot(r21[4], r11[4])
qc.cnot(r21[5], r11[5])
qc.cnot(r21[0], r11[4])
qc.cnot(r21[1], r11[5])

qc.cnot(r22[4], r11[0])
qc.cnot(r22[5], r11[1])
qc.cnot(r22[0], r11[0])
qc.cnot(r22[1], r11[1])

# classical controlled-swap u3+
qc.cswap(qreg_data[0], r21[4], r21[5])
qc.cswap(qreg_data[1], r21[0], r21[1])
qc.cswap(qreg_data[2], r22[4], r22[5])
qc.cswap(qreg_data[3], r22[0], r22[1])


# create initial data register state u2+
qc.cnot(r21[2], r21[1])
qc.cnot(r21[3], r21[5])
qc.cnot(r22[2], r22[1])
qc.cnot(r22[3], r22[5])

# swap address in u1+


qc.swap(r22[2], r11[0])
qc.swap(r22[3], r11[1])
qc.swap(r21[2], r11[4])
qc.swap(r21[3], r11[5])

qc.cswap(r11[3], inp[1], r11[5])
qc.cswap(r11[3], inp[0], r11[4])
qc.cswap(r11[2], inp[1], r11[1])
qc.cswap(r11[2], inp[0], r11[0])

qc.swap(add[1], inp[1])
qc.swap(add[0], inp[0])

qc.swap(inp[0], r11[2])
qc.swap(inp[1], r11[3])

qc.swap(add[3], inp[1])
qc.swap(add[2], inp[0])


offset = {
    "bus": 0,
    "address": 2,
    "input": 6,
    "router2.2": 8,
    "router2.1": 14,
    "router1.1": 20,
    "data": 26,
}

for data in qc.data:
    print(data[0].name, end=" ")
    for x in data[1]:
        print(x.index + offset[x.register.name], end=" ")
    print()