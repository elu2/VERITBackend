import pandas as pd
import numpy as np
import os
import pickle
import datetime

pat_dir = "./papers_as_tsv/"

# Check if this is the first time running the pipeline
if os.path.exists("./pat.log.pkl"):
    with open('pat.log.pkl', 'rb') as f:
        prev_pat = pickle.load(f)
else:
    prev_pat = []

# Get current snapshot of directory
next_pat = [x for x in os.listdir(pat_dir) if "PMC" in x]
# Files needed to run next
to_pat = np.setdiff1d(next_pat, prev_pat, assume_unique=True)

# Write out the files needed for the next run
with open('torun.log.pkl', 'wb') as f:
    pickle.dump(list(to_pat), f)

with open("runs.log", "a") as f:
    time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f.write(f"{time_now} (startup.py) Found {len(to_pat)} new files.\n")
