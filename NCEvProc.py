# Processes all NONE CONTROLLERs and concatenates into large csv file.

import pandas as pd
import os
import time
import csv
import datetime
from joblib import Parallel, delayed
import numpy as np

# Path to directory before papers_as_tsv/
base_path = "/xdisk/guangyao/elu2/REACHVisualization/"


def noneConcat(file):
    df = pd.read_csv(file, sep='\t', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8').astype(str)
    ev_df = df.iloc[:, [0, 1, 2, 3, 4, 17, 18]]
    none_df = ev_df.query("CONTROLLER=='NONE'").iloc[:, [3, 4]]
    joined = pd.merge(ev_df, none_df, left_on="INPUT", right_on="EVENT ID")

    joined_dict = joined.to_dict()
    joined_dict["EVENT_LABEL"] = []

    for i in range(len(joined_dict["CONTROLLER"])):
        if joined_dict["EVENT LABEL_x"][i] == "Regulation (Negative)":
            if joined_dict["EVENT LABEL_y"][i] == "Amount":
                joined_dict["EVENT_LABEL"].append("Activation (Positive)")
            elif joined_dict["EVENT LABEL_y"][i] == "Transcription":
                joined_dict["EVENT_LABEL"].append("Activation (Negative)")
            elif joined_dict["EVENT LABEL_y"][i] == "Ubiquitination":
                joined_dict["EVENT_LABEL"].append("Activation (Positive)")
            else:
                joined_dict["EVENT_LABEL"].append("Inconclusive")


        elif joined_dict["EVENT LABEL_x"][i] == "Regulation (Positive)":
            if joined_dict["EVENT LABEL_y"][i] == "Amount":
                joined_dict["EVENT_LABEL"].append("Activation (Negative)")
            elif joined_dict["EVENT LABEL_y"][i] == "Transcription":
                joined_dict["EVENT_LABEL"].append("Activation (Positive)")
            elif joined_dict["EVENT LABEL_y"][i] == "Ubiquitination":
                joined_dict["EVENT_LABEL"].append("Activation (Negative)")
            else:
                joined_dict["EVENT_LABEL"].append("Inconclusive")

    joined_dict["EVENT_LABEL"] = pd.Series(joined_dict["EVENT_LABEL"])
    joined_ev_df = pd.DataFrame(joined_dict)
    joined_ev_df = joined_ev_df.drop_duplicates(subset=["OUTPUT", "CONTROLLER", "SEEN IN", "EVENT_LABEL"]).reset_index(drop=True)
    trunc_df = joined_ev_df.iloc[:, [0, 1, 2, 3, 5, 6, 9]]

    return trunc_df


def all_NC_concat(paper_list):
    # Initialize csv file with column names
    base_df = pd.DataFrame()
    counter = 0

    # Loop through papers directory
    for file in paper_list:
        filename = os.fsdecode(file)
        file_path = paper_path + filename
        file_df = noneConcat(file_path)

        base_df = base_df.append(file_df, ignore_index=True)

        counter += 1
        if counter % 1000 == 0:
            base_df.to_csv('AllNC.csv', mode='a', header=False)
            base_df = pd.DataFrame()

    # Unload last iteration of <1000 papers
    base_df.to_csv('AllNC.csv', mode='a', header=False, index=False)


# Restructures dataframe to be compatible with other scripts
def conformity(csv_path):
    df = pd.read_csv(csv_path, sep=',', header=0, error_bad_lines=False, encoding='utf-8').iloc[:, 1:]
    df = df[["INPUT", "OUTPUT", "CONTROLLER", "EVENT ID_x", "EVENT_LABEL", "EVIDENCE", "SEEN IN"]]
    colnames = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "EVIDENCE", "SEEN_IN"]
    df.columns=colnames

    cleaned = df[~df.INPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.OUTPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.CONTROLLER.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.INPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.OUTPUT.str.contains("nan", na=False)]
    cleaned = cleaned[~cleaned.CONTROLLER.str.contains("nan", na=False)]
    cleaned = cleaned[~cleaned.OUTPUT.str.contains("{", na=False)]
    cleaned = cleaned.dropna()
    cleaned = cleaned.reset_index(drop=True)

    cleaned.to_csv('AllNC.csv', mode='w', header=True, index=False)


column_names = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT ID_x", "EVIDENCE", "SEEN IN", "EVENT_LABEL"]
base_df = pd.DataFrame(columns = column_names)
base_df.to_csv('AllNC.csv', mode='w', header=True)

paper_path = base_path + "papers_as_tsv/"
directory = os.fsencode(paper_path)
all_files = os.listdir(directory)
file_chunks = np.array_split(np.array(all_files), 40)

Parallel(n_jobs=-1)(delayed(all_NC_concat)(paper_list) for paper_list in file_chunks)

conformity(base_path + "AllNC.csv")
