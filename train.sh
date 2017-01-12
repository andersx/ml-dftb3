#!/usr/bin/env bash


SIGMA=10.0
LAMBDA=1e-5

NTRAIN=500

cd krr_machine

for atom in H C N O S
do
    ./generate_distance_matrix.py $NTRAIN $atom
    ./dump_alpha.py $SIGMA $LAMBDA
    mv X.npy trainings/$atom\_X.npy
    mv alpha.npy trainings/$atom\_alpha.npy
done

cd ..
