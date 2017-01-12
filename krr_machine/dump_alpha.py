#!/usr/bin/env python2

import sys
import numpy as np
from copy import deepcopy
from fml.math import cho_solve
from scipy.stats import pearsonr

if __name__ == "__main__":

    sigma = float(sys.argv[1])
    llambda = float(sys.argv[2])

    D  = np.load("D.npy")
    Y  = np.load("Y.npy")
   
    print "calculating kernel"
    s = (-0.5 / sigma**2)
    D *=s
    np.exp(D, D)

    for i in range(len(Y)):
        D[i,i] += llambda

    print "inverting"
    alpha = cho_solve(D, Y)
    np.save("alpha.npy", alpha)
