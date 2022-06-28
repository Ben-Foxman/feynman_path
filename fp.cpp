#include "Gate.cpp"
#include <map>
#include <iostream>
#include <fstream>
#include <vector>
#include <assert.h>
using namespace std::complex_literals;

map<string, Gate> gates;

int n, N;
map<int, complex<double>> state;

struct FeynmanNode  {
    int incoming, outgoing;
    string gateName;
};

void init_gates(){
    Gate* h = new Gate("h", 1, (complex<double>[]){1/sqrt(2), 1/sqrt(2), 1/sqrt(2), 1/sqrt(2)});
    Gate* x = new Gate("x", 1, (complex<double>[]){0, 1, 1, 0});
    Gate* y = new Gate("y", 1, (complex<double>[]){0, -1i, 1i, 0});
    Gate* z = new Gate("z", 1, (complex<double>[]){1, 0, 0, -1});
    Gate* s = new Gate("s", 1, (complex<double>[]){1, 0, 0, 1i});
    Gate* t = new Gate("t", 1, (complex<double>[]){1, 0, 0, 1/sqrt(2) + 1i/sqrt(2)});
    Gate* cx = new Gate("cx", 2, (complex<double>[]){1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0});
    Gate* cz = new Gate("cz", 2, (complex<double>[]){1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1});
    Gate* swap = new Gate("swap", 2, (complex<double>[]){1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1});
    Gate* ccx = new Gate("ccx", 3, (complex<double>[]){1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1});
    Gate* cswap = new Gate("cswap", 3, (complex<double>[]){1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1});

    gates["h"] =  *h;
    gates["x"] =  *x;
    gates["y"] =  *y;
    gates["z"] =  *z;
    gates["s"] =  *s;
    gates["t"] =  *t;
    gates["cx"] =  *cx;
    gates["cz"] =  *cz;
    gates["swap"] =  *swap;
    gates["ccx"] = *ccx;
    gates["cswap"] = *cswap;

}

// get kth LSB of i, where 0 <= i < N
int get_bit(int i, int k){
    return (1 << k) & i;
}

// flip kth LSB of i, where 0 <= i < N
int flip_bit(int i, int k){
    return (1 << k) ^ i;
}

int label(string name){
    if (name == "h") {return 0;}
    if (name == "x") {return 1;}
    if (name == "y") {return 2;}
    if (name == "z") {return 3;}
    if (name == "s") {return 4;}
    if (name == "t") {return 5;}
    if (name == "cx") {return 6;}
    if (name == "cz") {return 7;}
    if (name == "swap") {return 8;}
    if (name == "ccx") {return 9;}
    if (name == "cswap") {return 10;}
    return -1;
}



void process_gate(string name, vector<int> wires){
    map<int, complex<double>> newState;

    auto newStateUpdate = [&](int key, complex<double> value)
    {
        if (newState.contains(key)){
            newState[key] += value;
        }
        else {
            newState[key] = value;
        }
    };

    if (gates.contains(name)){
        assert(gates[name].get_n() == wires.size());
        switch (label(name))
        {
        case 0: // h
            for (const auto& [ket, amplitude]  : state)
                {
                    int newKet = flip_bit(ket, wires[0]);
                    switch (get_bit(ket, wires[0]))
                    {
                    case 0:
                        newStateUpdate(ket, (1/sqrt(2)) * amplitude);
                        newStateUpdate(newKet, (1/sqrt(2)) * amplitude);
                        break;
                    case 1:
                        cout << "no" << ket << endl;
                        newStateUpdate(ket, -1 * (1/sqrt(2)) * amplitude);
                        newStateUpdate(newKet, (1/sqrt(2)) * amplitude);
                        break;


                    }
                }
            break;
        case 1: // x
            for (const auto& [ket, amplitude]  : state)
                {
                    newStateUpdate(flip_bit(ket, wires[0]), amplitude);
                }
            break;
        case 2: // y
            for (const auto& [ket, amplitude]  : state)
                {
                    complex<double> sign = 1 - (2 * get_bit(ket, wires[0]));
                    newStateUpdate(flip_bit(ket, wires[0]), sign * (1i * amplitude));

                }
            break;
        case 3: // z
            for (const auto& [ket, amplitude]  : state)
                {
                    complex<double> coeff = get_bit(ket, wires[0]) ? -1 : 1;
                    newStateUpdate(ket, coeff * amplitude);

                }
            break;
        case 4: // s
            for (const auto& [ket, amplitude]  : state)
                {
                    complex<double> coeff = get_bit(ket, wires[0]) ? 1i : 1;
                    newStateUpdate(ket, coeff * amplitude);

                }
            break;
        case 5: // t
            for (const auto& [ket, amplitude]  : state)
                {
                    complex<double> coeff = get_bit(ket, wires[0]) ? (1.0 + 1i)/sqrt(2) : 1;
                    newStateUpdate(ket, coeff * amplitude);
                }
            break;
        case 6: // cx
            for (const auto& [ket, amplitude]  : state)
                {
                    if (get_bit(ket, wires[0])) {
                        newStateUpdate(flip_bit(ket, wires[1]), amplitude);
                    }
                    else {
                        newStateUpdate(ket, amplitude);
                    }
                }
            break;
        case 7: // cz
            for (const auto& [ket, amplitude]  : state)
                {
                    if (get_bit(ket, wires[0])) {
                        complex<double> coeff = get_bit(ket, wires[0]) ? -1 : 1;
                        newStateUpdate(ket, coeff * amplitude);
                    }
                    else {
                        newStateUpdate(ket, amplitude);
                    }
                }
            break;
        case 8: // swap
            for (const auto& [ket, amplitude]  : state)
                {
                    if (get_bit(ket, wires[0]) != get_bit(ket, wires[1])) {
                        newStateUpdate(flip_bit(flip_bit(ket, wires[0]), wires[1]), amplitude);
                    }
                    else {
                        newStateUpdate(ket, amplitude);
                    }
                }
            break;
        case 9: // ccx
            for (const auto& [ket, amplitude]  : state)
                {
                    if (get_bit(ket, wires[0]) && get_bit(ket, wires[1])) {
                        newStateUpdate(flip_bit(ket, wires[2]), amplitude);
                    }
                    else {
                        newStateUpdate(ket, amplitude);
                    }
                }
            break;
        case 10: // ccswap
            for (const auto& [ket, amplitude]  : state)
                {
                    if (get_bit(ket, wires[0]) && (get_bit(ket, wires[1]) != get_bit(ket, wires[2]))) {
                        newStateUpdate(flip_bit(flip_bit(ket, wires[1]), wires[2]), amplitude);
                    }
                    else {
                        newStateUpdate(ket, amplitude);
                    }
                }
            break;
        }
    }
    else {
        cout << "Error: Unknown Gate " << name <<  "- Currently Implemented gates are:" << endl;
    }
    state.erase(state.begin(), state.end());
    state.insert(newState.begin(), newState.end());
}


int main() {
    // 0. gate details
    init_gates();

    std::ifstream infile("in.txt");
    string line;
    bool first = true, second = false;
    while (std::getline(infile, line))
    {
        // 1. get size of program
        if (first) {
            n = stoi(line);
            N = pow(2, n);
            first = false;
            second = true;
        }
        // 2. get input state (zero state for now)
        else if (second) {
            state[0] = 1;
            second = false;
        }
        // 3. get gate sequence
        else {
            std::istringstream iss(line);
            string name;
            vector<int> wires;
            string wire;

            iss >> name;
            while (iss >> wire){
                assert(0 <= stoi(wire) && stoi(wire) < n);
                wires.push_back(stoi(wire));
            }
            process_gate(name, wires);
        }
    }

    for (const auto& [ket, amplitude]  : state){
        if (abs(amplitude) != 0){
            cout << "Ket:" << ket << endl;
            cout << "Amplitude:" << (amplitude.real() > -0.0 ? "+" : "") << amplitude.real() << (amplitude.imag() >= -0.0 ? "+" : "") << amplitude.imag() << "i" << endl;
        }

    }
}
