# Feynman Path Simulator in C++
This is an implementation of the Feynman Path Method for Quantum Circuit Simulation, supporting all Clifford gates and some non-Clifford gates. To run the simulator, build ```fp.cpp``` with std>=c++17, and then invoke
```
./OUTFILE <circuit INFILE>
```
to run. The optional flag ```-p``` can be passed in after the infile name to print the full state of the circuit after simulation. 

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

## Other Details of the Repo ##
- To compare this simulator's speed against Aaronson's CHP (CNOT-Hadamard-Phase) Simulator, I modified their original code, which can be found at https://www.scottaaronson.com/chp/. This modified version can be run the same as the Feynman Path simulator, just by building modified_chp.c. Note there is no new `-p` flag, but the original CLI options in Aaronson's original can still be invoked.
- The output folder contains some raw data of simulation output from the Feynman Path and CHP Simulators, and a plot demonstrating the exponential scaling of the Feynman Path Simulation (although absolute simulation time is still fast for low qubit counts). 
