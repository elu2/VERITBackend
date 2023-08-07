import pandas as pd
import os
from glob import glob

#Configure pickle files, directories
r_file = "/xdisk/guangyao/michellewei/PMC_OA_Processed/evidence.pkl"   #REACH evidence pickle
b_file = "/xdisk/guangyao/michellewei/BIOGRID_pickles/BIOGRID_evidence.pkl"   #BG evidence pickle
out_dir = "/xdisk/guangyao/michellewei/pmcbiogrid"  #Evidence directory
n_dir = 100   #Number of subdirectories to write evidence into

#Make the directory to write evidence files into
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

#Read in evidence df
r_df = pd.read_csv(r_file)
b_df = pd.read_pickle(b_file)
b_df_switched = b_df.rename(columns={"source":"target", "target":"source"})   #Switch source and target for bidirectional edge
full_b_df = pd.concat([b_df, b_df_switched]).drop_duplicates()
full_df = r_df.merge(full_b_df, how="outer", on=["source", "target"], suffixes=["_r", "_b"])
full_df = full_df.fillna("")
full_df["evidence"] = full_df["evidence_r"] + "&&&" + full_df["evidence_b"]  #Concatenate REACH and BG evidence

#Get lists of ev, target ID, source ID
ev_list = full_df["evidence"].tolist()
targets = full_df["target"].tolist()
sources = full_df["source"].tolist()

#Write evidence for each edge into a separate file, located in 1 of n subdirectories in out_dir
for i in range(len(ev_list)):
    delim = f"{sources[i]}_{targets[i]}.txt"
    ev = ev_list[i]
    dir_num=i%n_dir
    dir_name = f"{out_dir}/ev_{dir_num}"
    if not os.path.exists(dir_name):   
        os.mkdir(dir_name)
    filename = f"{dir_name}/{delim}"
    with open(filename, "w") as file:
        file.write(ev) 


    
      
