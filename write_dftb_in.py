#!/usr/bin/env python2

import sys
import numpy as np

from fml import Molecule
from fml.math import l2_distance
SLKO_PATH = "/home/andersx/parameters/3ob-3-1/"

CHARGE = "0"

# if len(sys.argv) > 2:
#    CHARGE = sys.argv[2]

ANGULAR_MOMENTUM = dict()
ANGULAR_MOMENTUM["Br"]  = "d"
ANGULAR_MOMENTUM["C"]   = "p"
ANGULAR_MOMENTUM["Ca"]  = "p"
ANGULAR_MOMENTUM["Cl"]  = "d"
ANGULAR_MOMENTUM["F"]   = "p"
ANGULAR_MOMENTUM["H"]   = "s"
ANGULAR_MOMENTUM["I"]   = "d"
ANGULAR_MOMENTUM["K"]   = "p"
ANGULAR_MOMENTUM["Mg"]  = "p"
ANGULAR_MOMENTUM["N"]   = "p"
ANGULAR_MOMENTUM["Na"]  = "p"
ANGULAR_MOMENTUM["O"]   = "p"
ANGULAR_MOMENTUM["P"]   = "d"
ANGULAR_MOMENTUM["S"]   = "d"
ANGULAR_MOMENTUM["Zn"]  = "d"

HUBBARD_DERIVS = dict()
HUBBARD_DERIVS["Br"] = -0.0573
HUBBARD_DERIVS["C"]  = -0.1492
HUBBARD_DERIVS["Ca"] = -0.034
HUBBARD_DERIVS["Cl"] = -0.0697
HUBBARD_DERIVS["F"]  = -0.1623
HUBBARD_DERIVS["H"]  = -0.1857
HUBBARD_DERIVS["I"]  = -0.0433
HUBBARD_DERIVS["K"]  = -0.0339
HUBBARD_DERIVS["Mg"] = -0.02
HUBBARD_DERIVS["N"]  = -0.1535
HUBBARD_DERIVS["Na"] = -0.0454
HUBBARD_DERIVS["O"]  = -0.1575
HUBBARD_DERIVS["P"]  = -0.14
HUBBARD_DERIVS["S"]  = -0.11
HUBBARD_DERIVS["Zn"] = -0.03



def get_slako_filename(type_a, type_b):

    filename = ""

    if len(type_a) == 1:

        filename += type_a.upper()
    elif len(type_a) == 2:

        s = ("" + type_a[0]).upper()
        filename += s
        s = ("" + type_a[1]).lower()
        filename += s

    else:

        print type_a

    filename += "-"

    if len(type_b) == 1:

        filename += type_b.upper()
    elif len(type_b) == 2:

        s = ("" + type_b[0]).upper()
        filename += s
        s = ("" + type_b[1]).lower()
        filename += s

    else:
        print type_b

    filename += ".skf"

    return filename


def get_atom_types(lines):

    atoms = []

    for line in lines[2:]:

        tokens = line.split()
        if not len(tokens) == 4:
            break
        
        atom = tokens[0]

        if atom not in atoms:
            atoms.append(atom)

    return atoms


def print_header(lines):

    atoms = get_atom_types(lines)

    print lines[0].split()[0], " C"

    print " ", 
    for atom in atoms:
        print atom, 

    print

    return

def generate_atoms_dictionary(lines):

    atoms = get_atom_types(lines)

    atom_dictionary = dict()
    
    for i, atom_type in enumerate(atoms):

        atom_dictionary[atom_type] = i + 1

    return atom_dictionary



if __name__ == "__main__":


    # print "Loading data ..."
    alpha = dict()
    alpha['H']  = np.load("qm7/H_alpha.npy")
    alpha['C']  = np.load("qm7/C_alpha.npy")
    alpha['N']  = np.load("qm7/N_alpha.npy")
    alpha['O']  = np.load("qm7/O_alpha.npy")
    alpha['S']  = np.load("qm7/S_alpha.npy")

    X = dict()
    X['H'] = np.load("qm7/H_X.npy")
    X['C'] = np.load("qm7/C_X.npy")
    X['N'] = np.load("qm7/N_X.npy")
    X['O'] = np.load("qm7/O_X.npy")
    X['S'] = np.load("qm7/S_X.npy")

    Ks = np.zeros((len(X)))

    # sigma = float(sys.argv[1]) 
    sigma = 10.0

    xyz_file = sys.argv[1]

    mol = Molecule()
    mol.from_xyz(xyz_file)
    mol.generate_atomic_coulomb_matrix()

    # for atom in ["H", "C", "N", "O", "S"]:
    #     print alpha[atom].shape
    #     print X[atom].shape

    # print

    Ys = np.zeros((mol.natoms))

    s = (-0.5 / sigma**2)
    # print "Running predicition ..."
    for a, atom in enumerate(mol.atomtypes):

        Xs = np.reshape(mol.atomic_coulomb_matrix[a], (len(mol.atomic_coulomb_matrix[a]),1))
        
        Ds = l2_distance(Xs, X[atom])

        Ds *=s
        Ks = np.array(np.exp(Ds))

        # Ks = np.reshape(Ks, (len(mol.atomic_coulomb_matrix[a])))
        Ys[a] = np.dot(Ks[0,:], alpha[atom])



    error = np.sum(Ys)
    Ys -= np.mean(Ys)

    #print "Final charges:"
    #for i, q in enumerate(Ys):
    #    print "%s  %12.8f" % (mol.atomtypes[i], q)

    f = open(xyz_file)
    lines = f.readlines()
    f.close()
    
    
    atom_dictionary = generate_atoms_dictionary(lines)
    
    print "Geometry = GenFormat {"
    print_header(lines)
    
    charge = 0 
    
    if "charge = " in lines[1]:
        tokens = lines[1].split()
        charge = float(tokens[2])

    for i, line in enumerate(lines[2:]):
    
        tokens = line.split()
    
        print "%4i %3i %16.10f %16.10f %16.10f " % \
            (i + 1 , atom_dictionary[tokens[0]], 
            float(tokens[1]),  float(tokens[2]), float(tokens[3]))
   
    print """}

Hamiltonian = DFTB {
    charge =""",
    print charge
    print """    SCC = Yes
    SlaterKosterFiles {"""

    atom_types = get_atom_types(lines)
    
    for atom_type1 in atom_types:
        for atom_type2 in atom_types:
    
            slko_filename = get_slako_filename(atom_type1, atom_type2)
    
            print "        " + atom_type1.upper() + "-" + atom_type2.upper() + \
                    " = \"" + SLKO_PATH + slko_filename + "\""
    
    print """    }
    MaxAngularMomentum {"""

    for atom_type in atom_types:
        print "        %s = \"%s\" " % ( atom_type, ANGULAR_MOMENTUM[atom_type])

    print """    }
    Filling = Fermi {
        Temperature [Kelvin] = 0.0
    }
    InitialCharges = {
        AllAtomCharges = {"""

    for q in Ys:
        print "            %12.8f" % (q)
    print """        }
    }
    SCCTolerance = 999999999999999999999999999999999999999999999.9
    MaxSCCIterations = 1
    ThirdOrderFull = Yes
    DampXH = Yes
    DampXHExponent = 4.00
    HubbardDerivs = {
"""
    for atom_type in atom_types:
        print "        %s = %s" % (atom_type, HUBBARD_DERIVS[atom_type])

    print """    }
}



Options {
    WriteBandOut = No
    WriteDetailedOut = Yes
    }

ParserOptions {
    ParserVersion = 4
    WriteHSDInput = No
}
"""
