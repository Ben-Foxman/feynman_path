# compute the partial trace of an n-qubit quantum state, given as a statevector dictionary of amplitudes for the observed and expected values
# 0 <= k < n: trace out all but first k qubits.
# compute <expected|Tr_R(observed)|expected> = <A|B|C>
# partial trace: http://www.thphy.uni-duesseldorf.de/~ls3/teaching/1515-QOQI/Additional/partial_trace.pdf

import numpy as np

def queryFidelity(k, observed, expected):
    print(observed, expected)
    print(observed == expected)
    # step 0: compute the effective expected output state 
    phi_out = dict()
    for i, j in expected.items():
        if i & ((2 ** k) - 1) in phi_out:
            phi_out[i & ((2 ** k) - 1)].append(np.abs(j))
        else:
            phi_out[i & ((2 ** k) - 1)] = [np.abs(j)]
    for i in phi_out:
        phi_out[i] = np.linalg.norm(phi_out[i], 2)



    # # step 0: compute the partial trace of the expected output state 
    # phi_out = dict()
    # # compare all basis state pairs
    # for k1, v1 in expected.items():
    #     for k2, v2 in expected.items():
    #         # if they are equal after the trace, then add their amplitdues 
    #         if k1 & ((2 ** k) - 1) == k2 & ((2 ** k) - 1):
    #             amplitude = k1 & ((2 ** k) - 1)
    #             if amplitude in phi_out:
    #                 phi_out[k1 & ((2 ** k) - 1)] += v1 * np.conjugate(v2)
    #             else: 
    #                 phi_out[k1 & ((2 ** k) - 1)] = v1 * np.conjugate(v2)


   
    # step 1: compute the partial trace of the observed output state 
    rho_out = dict()
    # compare all basis state pairs
    for k1, v1 in observed.items():
        for k2, v2 in observed.items():
            # if they are equal after the trace, then add their amplitdues 
            if k1 & ((2 ** k) - 1) == k2 & ((2 ** k) - 1):
                amplitude = k1 & ((2 ** k) - 1)
                if amplitude in rho_out:
                    rho_out[k1 & ((2 ** k) - 1)].append(v1 * np.conjugate(v2))
                else: 
                    rho_out[k1 & ((2 ** k) - 1)] = [v1 * np.conjugate(v2)]
    for i in rho_out:
        rho_out[i] = np.linalg.norm(rho_out[i], 2)

    ans = 0
    for k1, v1 in phi_out.items():
        for k2, v2 in rho_out.items():
            if k1 == k2:
                ans += np.conjugate(v1) * v2 * v1

    return np.real(ans)
    



    # for each state, first take the partial trace over the routers
    BC = dict()

    for k1, v1 in observed.items():
        for k2, v2 in observed.items():
            # split off first k bits (non-router bits)
            k1Traced = k1 & ((2 ** k) - 1)
            k2Traced = k2 & ((2 ** k) - 1)

            # check if traced out parts have the same state
            if k1 - k1Traced == k2 - k2Traced:     
                # if yes, compute inner product over all expected inputs 
                for k3, v3 in expected.items():
                    k3traced = k3 & ((2 ** k) - 1)
                    # all inner products have state 1, add to basis state k1traced
                    if k3traced == k1Traced:
                        # print(k1, k2, k3, v1, v2, v3)
                        if k1Traced in BC:
                            BC[k1Traced] += v1 * np.conjugate(v2) * v3
                        else:
                            BC[k1Traced] = v1 * np.conjugate(v2) * v3
            
    ABC = 0
    print(BC)
    for k1, v1 in expected.items():
        for k2, v2 in BC.items():
            if k1 & ((2 ** k) - 1) == k2:
                ABC += np.conjugate(v1) * v2

    return np.real(ABC) # we get a complex number with no imaginary part, so just discard it 

