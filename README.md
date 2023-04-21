# Feynman Path Simulation in C++
This is an implementation of the Feynman Path Method for Quantum Circuit Simulation, supporting all Clifford gates and some non-Clifford gates. We also implement the BB QRAM (from ) and a new Modified Dual-Rail QRAM, in formats which can be simulated.

To run the simulator, build ```fp.cpp``` with std>=c++17, and then invoke
```
./OUTFILE <circuit INFILE>
```
to run. The optional flag ```-p``` can be passed in after the infile name to print the full state of the circuit after simulation, and the optional flag 
```-d filename``` can be passed in after the infile name to write the state of the circuit to the file ```filename```.

### Valid INFILE Format ###

Valid circuit infiles are of the form
```
n
#
<gate1>
<gate2>
<gate3>
```
where n is the number of qubits in the circuit, # is a placeholder line, and <gate(s)> are valid gate names followed by the qubits the gates act on, for example `h 3` or `ccx 0 1 2`. 

## Other details ##
- To compare this simulator's speed against Aaronson's CHP (CNOT-Hadamard-Phase) Simulator, I modified their original code, which can be found at https://www.scottaaronson.com/chp/. This modified version can be run the same as the Feynman Path simulator, just by building modified_chp.c. Note there is no new `-p` flag, but the original CLI options in Aaronson's original code can still be invoked.
- ```circuit_processor.py``` defines a workflow for simulating noisy and noise-free versions of the QRAM architectures implemented in the "Circuits" directory. 
