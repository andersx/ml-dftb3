# ml-dftb3

Iteration-free SCC-DFTB3 using machine learning.

## How to use:

**Initialize the database:** As default you can initialize the machine using the QM7 database, hardcoded in the `generate_descriptors.py` script. Just run this script once, and you should find a file named `mols.cpickle`.

**Train the machine:** Run the `train.sh` to train the machine via the pickled data from the previous script.

**Run ML-DFTB3:** The program writes input for the `DFTB+` program. To generate the input for an ML-DFTB3 calculation do this `./write_dftb_in.py myfile.xyz > dftb_in.hsd`. The run `DFTB+` on the new input file.

That's it.

