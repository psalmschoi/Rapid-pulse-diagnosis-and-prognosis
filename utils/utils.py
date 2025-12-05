import numpy as np


def M_Diff(n, h=1.0, trans = False):
    if n < 3:
        raise ValueError("Size Error (n < 3)")

    D = np.zeros((n, n))

    diag_pos = np.ones(n - 1) * (1 / (2 * h))

    diag_neg = np.ones(n - 1) * (-1 / (2 * h))
    
    D += np.diag(diag_pos, k=1)
    D += np.diag(diag_neg, k=-1)
    
    D[0, 0] = -3 / (2 * h)
    D[0, 1] = 4 / (2 * h)
    D[0, 2] = -1 / (2 * h)
    
    D[n-1, n-3] = 1 / (2 * h)
    D[n-1, n-2] = -4 / (2 * h)
    D[n-1, n-1] = 3 / (2 * h)
    
    if trans :
        return D
    else :
        return D.T