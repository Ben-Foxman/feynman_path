#include <string>
#include <complex>
using namespace std;

class Gate {
    private:
        string name;
        int n;
        complex<double> computation_table[];
    public:
        // n: this is an n-qubit gate.
        // s: name of Gate.
        // computation_table: The evaluations <x|.|y> as x and y run over n qubit basis states
        // in lexicographic order.
        Gate() {}

        Gate(string s, int t, complex<double> table[]){
            name = s;
            n = t;
            for (int i = 0; i < pow(2, pow(2, n)); i++){
                computation_table[i] = table[i];
            }
        }
        string get_name(){
            return Gate::name;
        }
        int get_n(){
            return Gate::n;
        }
};
