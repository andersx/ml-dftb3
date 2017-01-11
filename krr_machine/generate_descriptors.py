#!/usr/bin/env python2


import os

import numpy as np
import ezpickle
from fml import Molecule


if __name__ == "__main__":

    xyz_dir = "/home/andersx/projects/ml-dftb3/qm7/xyz/"

    charges_txt = "/home/andersx/projects/ml-dftb3/qm7/dftb_charges.txt"

    charges = dict()

    f = open(charges_txt, "r")
    lines = f.readlines()
    f.close()

    for line in lines:
        filename = line[:8]
        q = np.array(eval(line[9:]))
        charges[filename] = q

    filenames = sorted(os.listdir(xyz_dir))

    np.random.seed(666)
    np.random.shuffle(filenames)

    mols = []

    for filename in filenames:

        print filename
        mol = Molecule()
        mol.read_xyz(xyz_dir + filename)
        molid = filename[-8:-4]
        mol.molid = int(molid)
        mol.generate_atomic_coulomb_matrix()
        mol.properties = charges[filename]

        mols.append(mol)

    ezpickle.save(mols, "mols.cpickle")

