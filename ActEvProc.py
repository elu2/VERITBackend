import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed
import csv

from html.parser import HTMLParser
from io import StringIO
import re
import datetime
import pickle


class TagStripper(HTMLParser):
    """ Use this class to strip markup and get the attributes of the tags as properties of the instance """
    def __init__(self, data:str):
        super().__init__()
        self._raw_sentence = StringIO()
        self._data = data
        self.feed(data)
        self.space_remover = re.compile(r'\s+')

    def handle_data(self, data: str) -> None:
        self._raw_sentence.write(data)

    @property
    def raw_sentence(self) -> str:
        return self.space_remover.sub(' ', self._raw_sentence.getvalue().strip())


def truncator(path):
    df = pd.read_csv(path, sep='\t', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8', dtype=str).astype(str)
    ev_df = df[spec_cols]
    return ev_df


def post_proc(df):
    # Remove rows that will be deferred to NCEvProc.py
    df = df[df.CONTROLLER != "NONE"]
    df = df[df["EVENT LABEL"].str.contains("Regulation", na=False) == False]
    # Remove :uaz: rows
    drop_rows = (df["INPUT"].str.contains(":uaz:") == False) * (df["OUTPUT"].str.contains(":uaz:") == False) * (df["CONTROLLER"].str.contains(":uaz:") == False)
    # Remove two double colon species
    drop_rows = drop_rows * (df["OUTPUT"].str.contains('{') == False)
    df = df[drop_rows]

    # Replace associations labels with conventional labels
    df["EVENT LABEL"] = df["EVENT LABEL"].replace({"Association (Positive)": "Activation (Positive)",
                                                   "Association (Negative)": "Activation (Negative)",
                                                   "Association (UNKNOWN)": "Inconclusive"})
    
    # Remove HTML artifacts from evidence
    df["EVIDENCE"] = df["EVIDENCE"].apply(lambda x: TagStripper(x).raw_sentence)

    return df


def concat_papers(paper_list, paper_path="./papers_as_tsv/"):
    # Loop through papers directory
    for file in paper_list:
        file_path = paper_path + file
        file_df = truncator(file_path)

        file_df.to_csv('NewAllAct.csv', mode='a', header=False, index=False)

    return None


if __name__ == "__main__":
    # Columns to concat on
    spec_cols = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT ID", "EVENT LABEL", "EVIDENCE", "SEEN IN"]

    # Initialize empty file to append to
    init_df = pd.DataFrame(columns=spec_cols)
    if not os.path.exists("NewAllAct.csv"):
        init_df.to_csv("NewAllAct.csv", index=False)

    # get paper paths and chunk for parallelization
    with open('torun.log.pkl', 'rb') as f:
        to_run = pickle.load(f)
    to_run = [x for x in to_run if "PMC" in x]
    file_chunks = np.array_split(np.array(to_run), 40)

    Parallel(n_jobs=-1)(delayed(concat_papers)(paper_list) for paper_list in file_chunks)
    
    # post-processing of files
    aa_df = pd.read_csv("NewAllAct.csv", encoding='utf-8')
    aa_df = post_proc(aa_df)
    aa_df.to_csv("NewAllAct.csv", index=False)
    
    with open("runs.log", "w") as f:
        time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"{time_now} (ActEvProc.py) Finished.\n")
