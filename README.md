# Feynman Path Simulator in C++
This is an implementation of the Feynman Path Method for Quantum Circuit Simulation, supporting all Clifford gates and some non-Clifford gates. To run the simulator, build ```fp.cpp```, and then invoke
```
./OUTFILE <circuit INFILE>
```
to run. The optional flag ```-p``` can be passed in after the infile name to print the full state of the circuit after simulation. 

### Valid INFILE Format ###


## Other Details of the Repo ##
- To compare this simulator's speed against Aaronson's CHP (CNOT-Hadamard-Phase) Simulator, I modified their original code, which can be found at https://www.scottaaronson.com/chp/. This modified version can be run the same as the Feynman Path simulator, just by building modified_chp.c. Note there is no new `-p`, but the original CLI options in Aaronson's original can still be invoked.
- 
