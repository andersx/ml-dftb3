#!/usr/bin/env python2

import sys
import numpy as np

from fml import Molecule
from fml.math import l2_distance

if __name__ == "__main__":


    print "Loading data ..."
    alpha = dict()
    alpha['H']  = np.load("trainings/H_alpha.npy")
    alpha['C']  = np.load("trainings/C_alpha.npy")
    alpha['N']  = np.load("trainings/N_alpha.npy")
    alpha['O']  = np.load("trainings/O_alpha.npy")
    alpha['S']  = np.load("trainings/S_alpha.npy")

    X = dict()
    X['H'] = np.load("trainings/H_X.npy")
    X['C'] = np.load("trainings/C_X.npy")
    X['N'] = np.load("trainings/N_X.npy")
    X['O'] = np.load("trainings/O_X.npy")
    X['S'] = np.load("trainings/S_X.npy")

    Ks = np.zeros((len(X)))

    sigma = float(sys.argv[1])
    llambda = float(sys.argv[2])
    xyz_file = sys.argv[3]

    mol = Molecule()
    mol.read_xyz(xyz_file)
    mol.generate_atomic_coulomb_matrix()

    Ys = np.zeros((mol.natoms))

    s = (-0.5 / sigma**2)

    print "Running predicition ..."
    for a, atom in enumerate(mol.atomtypes):

        Xs = np.reshape(mol.atomic_coulomb_matrix[a], (len(mol.atomic_coulomb_matrix[a]),1))
        
        Ds = l2_distance(Xs, X[atom])
        Ds *=s
        np.array(np.exp(Ds, Ds))

        Ys[a] = np.dot(Ds[0,:], alpha[atom])

    error = np.sum(Ys)
    Ys -= np.mean(Ys)

    print "Final charges:"
    for i, q in enumerate(Ys):
        print "%s  %12.8f" % (mol.atomtypes[i], q)
