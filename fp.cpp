#include <string>
#include <complex>
#include <map>
#include <iostream>
#include <fstream>
#include <vector>
#include <assert.h>
#include <string_view>
#include <bitset>
#include <algorithm>
#include "BigInt.hpp"
using namespace std;
using namespace std::complex_literals;

map<string, int> gates;

int n;
BigInt N;
BigInt gate_num = 0, computation_num = 0;
map<BigInt, complex<double>> state;

void init_gates()
{
    gates["h"] = 1;
    gates["x"] = 1;
    gates["y"] = 1;
    gates["z"] = 1;
    gates["s"] = 1;
    gates["t"] = 1;
    gates["cx"] = 2;
    gates["cz"] = 2;
    gates["swap"] = 2;
    gates["ccx"] = 3;
    gates["cswap"] = 3;
    gates["sdg"] = 1;
    gates["tdg"] = 1;
}

string format_state(BigInt ket, complex<double> amplitude)
{
    double real = amplitude.real() != -0.0 ? amplitude.real() : 0;
    double imag = amplitude.imag() != -0.0 ? amplitude.imag() : 0;
    string s = "";
    if (real != 0 || imag != 0)
    {
        if (real != 0)
        {
            s.append(to_string(real));
        }
        if (imag > 0 && real != 0)
        {
            s.append("+");
        }
        if (imag != 0)
        {
            s.append(to_string(imag)).append("i");
        }
        s.append("|" + ket.to_string() + ">");
        s.append("\n");
    }

    return s;
}

int label(string name)
{
    if (name == "h")
    {
        return 0;
    }
    if (name == "x")
    {
        return 1;
    }
    if (name == "y")
    {
        return 2;
    }
    if (name == "z")
    {
        return 3;
    }
    if (name == "s")
    {
        return 4;
    }
    if (name == "t")
    {
        return 5;
    }
    if (name == "cx")
    {
        return 6;
    }
    if (name == "cz")
    {
        return 7;
    }
    if (name == "swap")
    {
        return 8;
    }
    if (name == "ccx")
    {
        return 9;
    }
    if (name == "cswap")
    {
        return 10;
    }
    if (name == "sdg")
    {
        return 11;
    }
    if (name == "tdg")
    {
        return 12;
    }
    return -1;
}

// TODO: make BigInt compatibility work
//  get kth LSB of i, where 0 <= i < N
int get_bit(BigInt i, int k)
{
    BigInt b = i;
    for (int j = 0; j < k; j++)
    {
        b /= 2;
    }
    return (b % 2).to_int();
}

// flip kth LSB of i, where 0 <= i < N
BigInt flip_bit(BigInt i, int k)
{
    int b = 1 - 2 * get_bit(i, k);
    BigInt c = pow(BigInt(2), k);
    return BigInt(i) + BigInt(b) * c;
}

void process_gate(string name, vector<int> wires)
{
    std::map<BigInt, complex<double>> newState;

    auto newStateUpdate = [&](BigInt key, complex<double> value)
    {
        computation_num += 1;
        if (newState.count(key))
        {
            newState[key] += value;
        }
        else
        {
            newState[key] = value;
        }
    };

    if (gates.count(name))
    {
        assert(gates[name] == wires.size());
        assert(wires.size() == 1 || adjacent_find(wires.begin(), wires.end()) == wires.end());
        gate_num += 1;
        switch (label(name))
        {
        case 0: // h
            for (const auto &[ket, amplitude] : state)
            {
                BigInt newKet = flip_bit(ket, wires[0]);
                switch (get_bit(ket, wires[0]))
                {
                case 0:
                    newStateUpdate(ket, (1 / sqrt(2)) * amplitude);
                    newStateUpdate(newKet, (1 / sqrt(2)) * amplitude);
                    break;
                case 1:
                    newStateUpdate(ket, -1 * (1 / sqrt(2)) * amplitude);
                    newStateUpdate(newKet, (1 / sqrt(2)) * amplitude);
                    break;
                }
            }
            break;
        case 1: // x
            for (const auto &[ket, amplitude] : state)
            {
                newStateUpdate(flip_bit(ket, wires[0]), amplitude);
            }
            break;
        case 2: // y
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> sign = 1 - (2 * get_bit(ket, wires[0]));
                newStateUpdate(flip_bit(ket, wires[0]), sign * (1i * amplitude));
            }
            break;
        case 3: // z
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> coeff = get_bit(ket, wires[0]) ? -1 : 1;
                newStateUpdate(ket, coeff * amplitude);
            }
            break;
        case 4: // s
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> coeff = get_bit(ket, wires[0]) ? 1i : 1;
                newStateUpdate(ket, coeff * amplitude);
            }
            break;
        case 5: // t
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> coeff = get_bit(ket, wires[0]) ? (1.0 + 1i) / sqrt(2) : 1;
                newStateUpdate(ket, coeff * amplitude);
            }
            break;
        case 6: // cx
            for (const auto &[ket, amplitude] : state)
            {
                if (get_bit(ket, wires[0]))
                {
                    newStateUpdate(flip_bit(ket, wires[1]), amplitude);
                }
                else
                {
                    newStateUpdate(ket, amplitude);
                }
            }
            break;
        case 7: // cz
            for (const auto &[ket, amplitude] : state)
            {
                if (get_bit(ket, wires[0]))
                {
                    complex<double> coeff = get_bit(ket, wires[0]) ? -1 : 1;
                    newStateUpdate(ket, coeff * amplitude);
                }
                else
                {
                    newStateUpdate(ket, amplitude);
                }
            }
            break;
        case 8: // swap
            for (const auto &[ket, amplitude] : state)
            {
                if (get_bit(ket, wires[0]) != get_bit(ket, wires[1]))
                {
                    newStateUpdate(flip_bit(flip_bit(ket, wires[0]), wires[1]), amplitude);
                }
                else
                {
                    newStateUpdate(ket, amplitude);
                }
            }
            break;
        case 9: // ccx
            for (const auto &[ket, amplitude] : state)
            {
                if (get_bit(ket, wires[0]) && get_bit(ket, wires[1]))
                {
                    newStateUpdate(flip_bit(ket, wires[2]), amplitude);
                }
                else
                {
                    newStateUpdate(ket, amplitude);
                }
            }
            break;
        case 10: // ccswap
            for (const auto &[ket, amplitude] : state)
            {
                if (get_bit(ket, wires[0]) && (get_bit(ket, wires[1]) != get_bit(ket, wires[2])))
                {
                    newStateUpdate(flip_bit(flip_bit(ket, wires[1]), wires[2]), amplitude);
                }
                else
                {
                    newStateUpdate(ket, amplitude);
                }
            }
            break;
        case 11: // sdg
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> coeff = get_bit(ket, wires[0]) ? -1i : 1;
                newStateUpdate(ket, coeff * amplitude);
            }
            break;
        case 12: // tdg
            for (const auto &[ket, amplitude] : state)
            {
                complex<double> coeff = get_bit(ket, wires[0]) ? (1.0 - 1i) / sqrt(2) : 1;
                newStateUpdate(ket, coeff * amplitude);
            }
            break;
        }
    }
    else
    {
        cout << "Error: Unknown Gate " << name << "- Currently Implemented gates are: ";
        for (std::map<string, int>::iterator it = gates.begin(); it != gates.end(); ++it)
        {
            cout << it->first << " ";
        }
        cout << endl;
    }
    state.erase(state.begin(), state.end());
    state.insert(newState.begin(), newState.end());
}

int main(int argc, char **argv)
{
    // 0. gate details
    init_gates();

    std::ifstream infile("circuits/" + string(argv[1]));
    string line;
    bool first = true, second = false;

    // auto start = chrono::steady_clock::now();

    while (std::getline(infile, line))
    {
        // 1. get size of program
        if (first)
        {
            n = stoi(line);
            N = pow(BigInt(2), n);
            first = false;
            second = true;
        }
        // 2. get input state (TODO? zero state for now)
        else if (second)
        {
            state[0] = 1;
            second = false;
        }
        // 3. get gate sequence
        else
        {
            std::istringstream iss(line);
            string name;
            vector<int> wires;
            string wire;

            iss >> name;
            while (iss >> wire)
            {
                if (wire.compare("//") == 0) // comments
                {
                    break;
                }
                try
                {
                    stoi(wire);
                }
                catch (std::exception &e)
                {
                    cout << "BAD WIRE " << wire << "NAME " << name << endl;
                }
                assert(0 <= stoi(wire) && stoi(wire) < n);
                wires.push_back(stoi(wire));
            }
            process_gate(name, wires);
        }
    }
    // auto end = chrono::steady_clock::now();

    // auto exectime = chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();

    if (argc > 2 && string(argv[2]) == "-p")
    {
        cout << "--- Feynman Path Simulator ---" << endl
             << endl;
    }

    ofstream data;
    if (argc > 3 && string(argv[2]) == "-d")
    {
        data.open("data/" + string(argv[3]), fstream::out);
    }

    for (const auto &[ket, amplitude] : state)
    {
        if (argc > 3 && string(argv[2]) == "-d")
        {
            data << ket << "," << amplitude << endl;
        }
        if (argc > 2 && string(argv[2]) == "-p")
        {
            cout << format_state(ket, amplitude);
        }
    }
    if (argc > 2 && string(argv[2]) == "-p")
    {
        cout << endl;
        cout << "Gate count: " << gate_num << endl;
        cout << "Feynman Path Edges: " << computation_num << endl
             << endl;
        // cout << "Execution Time: " << exectime / 1000000000.0 << " seconds" << endl;
    }

    // write filename, exectime to outfile
    // ofstream runtime("bboutput.csv", fstream::app);

    // runtime << "fp, " << argv[1] << ", " << exectime / 1000000000.0 << " seconds" << endl;
}
