import pandas as pd
import os
import time
import csv
import datetime
from joblib import Parallel, delayed
import numpy as np

base_path = "/xdisk/guangyao/elu2/REACHVisualization/"


def truncator(path):
    df = pd.read_csv(path, sep='\t', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8').astype(str)
    ev_df = df.iloc[:, [0, 1, 2, 3, 4, 17, 18]]
    return ev_df


def all_Act_concat(paper_list):
    base_df = pd.DataFrame()
    counter = 0

    # Loop through papers directory
    for file in paper_list:
        filename = os.fsdecode(file)
        file_path = paper_path + filename

        file_df = truncator(file_path)
        base_df = base_df.append(file_df, ignore_index=True)

        counter += 1
        if counter % 1000 == 0:
            base_df.to_csv('AllAct.csv', mode='a', header=False)
            base_df = pd.DataFrame()

    # Unload last iteration of <1000 papers
    base_df.to_csv('AllAct.csv', mode='a', header=False, index=False)


def cleaner(csv_path):
    df = pd.read_csv(csv_path, sep=',', header=0, encoding='utf-8', error_bad_lines=False).iloc[:, 1:]

    no_none = df.query('CONTROLLER!="NONE"').reset_index(drop=True)
    no_pos_reg = no_none.query('EVENT_LABEL!="Regulation (Positive)"').reset_index(drop=True)
    no_neg_reg = no_pos_reg.query('EVENT_LABEL!="Regulation (Negative)"').reset_index(drop=True)

    cleaned = no_neg_reg[~no_neg_reg.INPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.OUTPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.CONTROLLER.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.INPUT.str.contains("uaz", na=False)]
    cleaned = cleaned[~cleaned.OUTPUT.str.contains("nan", na=False)]
    cleaned = cleaned[~cleaned.CONTROLLER.str.contains("nan", na=False)]
    cleaned = cleaned.dropna()
    cleaned = cleaned.reset_index(drop=True)

    cleaned.to_csv("AllAct.csv", mode='w', header=True, index=False)


# Initialize csv file with column names
column_names = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "EVIDENCE", "SEEN_IN"]
base_df = pd.DataFrame(columns = column_names)
base_df.to_csv('AllAct.csv', mode='w', header=True)

paper_path = base_path + "papers_as_tsv/"
directory = os.fsencode(paper_path)
all_files = os.listdir(directory)
file_chunks = np.array_split(np.array(all_files), 40)

Parallel(n_jobs=-1)(delayed(all_Act_concat)(paper_list) for paper_list in file_chunks)

cleaner(base_path + "AllAct.csv")
