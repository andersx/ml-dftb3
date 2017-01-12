#!/usr/bin/env python2

import numpy as np
import ezpickle
from fml.math import l2_distance
import sys

if __name__ == "__main__":


    natoms = int(sys.argv[1])

    mols = ezpickle.load("mols.cpickle")

    target = sys.argv[2]

    X = []
    Y = []

    for mol in mols:

        # print mol.molid

        for i in range(mol.natoms):

            if mol.atomtypes[i] == target:
            # if True:

                if len(Y) > natoms - 1:
                    break
                X.append(mol.atomic_coulomb_matrix[i])
                Y.append(mol.properties[i])

                    

    X = np.array(X)
    Y = np.array(Y)
    print "Total atoms:", len(Y)

    X = np.transpose(X)

    np.save("Y.npy", Y)
    np.save("X.npy", X)

    print "calculating distance matrix"
    D = l2_distance(X, X)

    np.save("D.npy", D)

