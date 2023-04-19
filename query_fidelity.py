import numpy as np

# goal: take the inner product between the observed and expected states.
def queryFidelity(observed, expected):
    ans = 0 
    for k1, v1 in observed.items():
        if k1 in expected:
            ans += v1 * np.conjugate(expected[k1])
    return np.abs(ans) ** 2

    
