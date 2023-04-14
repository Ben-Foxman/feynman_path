import numpy as np

# goal: take the inner product between the observed and expected states.
def queryFidelity(k, observed, expected):
    ans = 0 
    for k1, v1 in observed.items():
        if k1 in expected:
            ans += v1 * np.conjugate(expected[k1])
    return np.abs(ans) ** 2

    # print("The same state:", observed == expected)
    # # step 0: compute the effective expected output state 
    # phi_out = dict()
    # for k1, v1 in observed.items():
    #     for k2, v2 in observed.items():
    #         # if they are equal after the trace, then add their amplitdues 
    #         if k1 & ((2 ** k) - 1) == k2 & ((2 ** k) - 1):
    #             amplitude = k1 & ((2 ** k) - 1)
    #             if amplitude in phi_out:
    #                 phi_out[k1 & ((2 ** k) - 1)] += v1 * np.conjugate(v2)
    #             else: 
    #                 phi_out[k1 & ((2 ** k) - 1)] = v1 * np.conjugate(v2)
    # for i in phi_out:
    #     phi_out[i] = np.sqrt(phi_out[i])

    # # step 1: compute the partial trace of the observed output state 
    # rho_out = dict()
    # # compare all basis state pairs
    # for k1, v1 in observed.items():
    #     for k2, v2 in observed.items():
    #         # if they are equal after the trace, then add their amplitdues 
    #         if k1 & ((2 ** k) - 1) == k2 & ((2 ** k) - 1):
    #             amplitude = k1 & ((2 ** k) - 1)
    #             if amplitude in rho_out:
    #                 rho_out[k1 & ((2 ** k) - 1)] += v1 * np.conjugate(v2)
    #             else: 
    #                 rho_out[k1 & ((2 ** k) - 1)] = v1 * np.conjugate(v2)
    # for i in rho_out:
    #     rho_out[i] =  np.sqrt(rho_out[i])

    # print("Traced observed:", [(bin(k)[2:], v) for k, v in phi_out.items()])
    # print("Traced expected:", [(bin(k)[2:], v) for k, v in rho_out.items()])
    # # add up all the ampltidues
    # ans = 0
    # for k1, v1 in phi_out.items():
    #     for k2, v2 in rho_out.items():
    #         if k1 == k2:
    #             ans += v2 * v1

    # # take the norm squared
    # return np.abs(ans) ** 2
    
