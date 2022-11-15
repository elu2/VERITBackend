#!/bin/bash

#SBATCH --job-name=RV
#SBATCH --mincpus=18
#SBATCH --mem-per-cpu=6GB
#SBATCH --time=12:00:00
#SBATCH --partition=standard
#SBATCH --account=

cd 

module load python/3.9/3.9.10

python3 ActEvProc.py
python3 NCEvProc.py
python3 GenProc.py
python3 pickler.py
