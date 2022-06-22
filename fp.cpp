#include <map>
#include <iostream>
#include <cassert>
#include <fstream>
#include <math.h>
#include <string>
using namespace std;

enum Gate {
    X=0, Y=1, Z=2, H=3, CX=4, CCX=5, CSWAP=6,
};

std::string names[] =
{
    "x",
    "y",
    "z",
    "h",
};


struct FeynmanEdge {
    int incoming, outgoing;
    Gate gate;

    // comparison operators so we can use as hashmap keys.
    bool operator==(const FeynmanEdge &o) const {
        return incoming == o.incoming && outgoing == o.outgoing && gate == o.gate;
    }

    bool operator<(const FeynmanEdge &o) const {
        return incoming < o.incoming || (incoming == o.incoming && outgoing < o.outgoing) || (incoming == o.incoming && outgoing == o.outgoing && gate < o.gate);
    }

    // print override
    friend ostream& operator<<(ostream& os, const FeynmanEdge& f){
        os << '<' << f.incoming << '|' << names[f.gate] << '|' << f.outgoing << '>';
        return os;
    }
};


float singleQubitAmplitudes[2][2][4] = {
    {
        {0, 0, 1, 0.5}, //<0|.|0>
        {1, 1, 0, 0.5}  //<0|.|1>
    },
    {
        {1, 1, 0, 0.5}, //<1|.|0>
        {0, 0, 1, 0.5}  //<1|.|1>
    }
};

// Irreducible Edges - Non-Tensor Product Gates
map<FeynmanEdge, float> primitiveEdges;

void populateEdges(){
    // single qubit natives
    for (int i = 0; i < 2; i++){
        for (int j = 0; j < 2; j++){
            for (int k = 0; k < 4; k++){
                FeynmanEdge f;
                f.incoming = i;
                f.gate = static_cast<Gate>(k);
                f.outgoing = j;
                primitiveEdges[f] = singleQubitAmplitudes[i][j][k];
            }
        }

    }

}

int main() {

    cout << "--Feynman Path Simulator--" << endl;
    populateEdges();

    // check all the primitive edges
    for (const auto& [k, v]  : primitiveEdges)
    {
        cout << "|" << k << "|" << "^2" << " : " << v << endl;
    }

}
