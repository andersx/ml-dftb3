#!/usr/bin/env bash

./generate_distance_matrix.py 20000 H
./dump_alpha.py 10.0 1e-5
mv X.npy trainings/H_X.npy
mv alpha.npy trainings/H_alpha.npy

./generate_distance_matrix.py 20000 C
./dump_alpha.py 10.0 1e-5
mv X.npy trainings/C_X.npy
mv alpha.npy trainings/C_alpha.npy

./generate_distance_matrix.py 20000 N
./dump_alpha.py 10.0 1e-5
mv X.npy trainings/N_X.npy
mv alpha.npy trainings/N_alpha.npy

./generate_distance_matrix.py 20000 O
./dump_alpha.py 10.0 1e-5
mv X.npy trainings/O_X.npy
mv alpha.npy trainings/O_alpha.npy

./generate_distance_matrix.py 20000 S
./dump_alpha.py 10.0 1e-5
mv X.npy trainings/S_X.npy
mv alpha.npy trainings/S_alpha.npy
