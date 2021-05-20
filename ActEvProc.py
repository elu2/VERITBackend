import pandas as pd
import os
import time
import datetime

base_path = "/xdisk/guangyao/REACH2/REACHVisualization/"


def truncator(path):
    df = pd.read_csv(path, sep='\t', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8')
    ev_df = df.iloc[:, [0, 1, 2, 3, 4, 17, 18]]
    return ev_df


def all_Act_concat(base_path):
    paper_path = base_path + "papers_as_tsv/"
    directory = os.fsencode(paper_path)

    # Initialized housekeeping values
    counter = 0
    new_ref = time.time()
    time_diffs = []

    # Initialize csv file with column names
    column_names = ["INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "EVIDENCE", "SEEN_IN"]
    base_df = pd.DataFrame(columns = column_names)
    base_df.to_csv('AllAct.csv', mode='w', header=True)
    base_df = pd.DataFrame()

    # Loop through papers directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = paper_path + filename
        
        file_df = truncator(file_path)
        base_df = base_df.append(file_df, ignore_index=True)

        counter += 1
        if counter % 1000 == 0:
            end_time = time.time()

            time_diff = end_time - new_ref
            time_diffs.append(time_diff)

            with open("AllAct.log", "a") as log_file:
                log_file.write(f"{datetime.datetime.now()}: Passed {counter} papers. Took {time_diff} seconds.\n")

            base_df.to_csv('AllAct.csv', mode='a', header=False)
            base_df = pd.DataFrame()

            new_ref = time.time()

    # Unload last iteration of <1000 papers
    base_df.to_csv('AllAct.csv', mode='a', header=False)
    with open("AllAct.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: Passed remaining {counter%1000} papers. Completed.\n")
        
        
def cleaner(csv_path):
    df = pd.read_csv(csv_path, sep=',', header=0, quoting=csv.QUOTE_NONE, encoding='utf-8').iloc[:, 1:]
    
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
    
    
all_Act_concat(base_path)
cleaner(base_path + "AllAct.csv")
