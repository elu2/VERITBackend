import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed
import csv


def truncator(path):
    df = pd.read_csv(path, sep='\t', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8', dtype=str).astype(str)
    ev_df = df[spec_cols]
    return ev_df


def net_event(df):
    nc_df = df[df["EVENT LABEL"].str.contains("Activation") == False]
    id_df = nc_df[nc_df["CONTROLLER"] == "NONE"][["EVENT ID", "EVENT LABEL"]]
    nc_df = nc_df.merge(id_df, left_on="INPUT", right_on="EVENT ID", suffixes=("", " INIT"))

    # Define maps to replace values with
    map_dict_el = {"Regulation (Negative)": 1, "Regulation (Positive)": -1}
    map_dict_eli = {"Transcription": 1, "Amount": 1, "DecreaseAmount": -1, "Ubiquitination": -1}
    final_map = {1: "Activation (Positive)", -1: "Activation (Negative)", 0: "Inconclusive"}
    
    # Only some events are hardcoded. The others are treated as inconclusive
    all_events = list(set(nc_df["EVENT LABEL INIT"]))
    for event in all_events:
        if event not in map_dict_eli.keys():
            map_dict_eli[event] = 0
    all_events = list(set(nc_df["EVENT LABEL"]))
    for event in all_events:
        if event not in map_dict_el.keys():
            map_dict_eli[event] = 0

    # Replace events with numerical "directions"
    nc_df = nc_df.replace({"EVENT LABEL": map_dict_el})
    nc_df = nc_df.replace({"EVENT LABEL INIT": map_dict_eli})

    # Get net direction of the paired interactions
    nc_df["EVENT LABEL"] = nc_df["EVENT LABEL"] * nc_df["EVENT LABEL INIT"]

    # finally replace values
    nc_df = nc_df.replace({"EVENT LABEL": final_map})
    nc_df = nc_df.drop(["EVENT ID INIT", "EVENT LABEL INIT"], axis=1)
    
    return nc_df


def post_proc(df):
    # Remove NONE controllers
    df = df[df.CONTROLLER != "NONE"]
    # Remove regulation event labels
    df = df[df["EVENT LABEL"].str.contains("Regulation", na=False) == False]
    # Remove :uaz: rows
    drop_rows = (df["INPUT"].str.contains(":uaz:") == False) * (df["OUTPUT"].str.contains(":uaz:") == False) * (df["CONTROLLER"].str.contains(":uaz:") == False)
    # Remove two double colon species
    drop_rows = drop_rows * (df["OUTPUT"].str.contains('{') == False)

    df = df[drop_rows]

    return df


def concat_papers(paper_list, paper_path="./papers_as_tsv/"):
    # Loop through papers directory
    for file in paper_list:
        file_path = paper_path + file
        file_df = truncator(file_path)
        file_df = net_event(file_df)
        print(file)

        file_df.to_csv('AllNC.csv', mode='a', header=False, index=False)

    return None


if __name__ == "__main__":
    # Columns to concat on
    spec_cols = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT ID", "EVENT LABEL", "EVIDENCE", "SEEN IN"]

    # Initialize empty file to append to
    init_df = pd.DataFrame(columns=spec_cols)
    if not os.path.exists("AllNC.csv"):
        init_df.to_csv("AllNC.csv", index=False)

    # get paper paths and chunk for parallelization
    paper_path = "./papers_as_tsv/"
    all_files = [x for x in os.listdir(paper_path) if "PMC" in x]
    file_chunks = np.array_split(np.array(all_files), 40)

    Parallel(n_jobs=1)(delayed(concat_papers)(paper_list) for paper_list in file_chunks)
    
    # post-processing of files
    aa_df = pd.read_csv("AllNC.csv", encoding='utf-8')
    aa_df = post_proc(aa_df)
    aa_df.to_csv("AllNC.csv", index=False)
