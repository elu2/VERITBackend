# Main purpose: Create ev_id.csv which contains OUTPUT id, CONTROLLER id, and a large corpus of evidence.

import pandas as pd

# Function to get an ID from a species
def into_id(string):
    split_string = string.split(":")
    split_id = split_string[-2] + ":" + split_string[-1]
    
    if "." in split_id:
        split_id = split_id.split(".")[0]
    
    return split_id


# Read in and combine the two important csv files.
AllAct_df = pd.read_csv('AllAct.csv', encoding='utf-8')
AllNC_df = pd.read_csv("AllNC.csv", encoding='utf-8')
All_df = AllAct_df.append(AllNC_df, ignore_index=True)

# Trims off curly brackets in anomalies
All_df["INPUT"] = All_df["INPUT"].str.strip("{}")
All_df["OUTPUT"] = All_df["OUTPUT"].str.strip("{}")
All_df["CONTROLLER"] = All_df["CONTROLLER"].str.strip("{}")

# Converting to dictionary for a more workable format
ev_df_dict = All_df.to_dict()

# Adds new ID columns to dictionary
ev_df_dict["OUTPUT_ID"] = []
ev_df_dict["CONTROLLER_ID"] = []

# Store indexes where INPUT is an EVENT_ID. Nothing is done with this as of now.
anomalies = []

# Populates the new ID columns
for i in range(len(ev_df_dict["OUTPUT"])):
    try:
        ev_df_dict["OUTPUT_ID"].append(into_id(ev_df_dict["OUTPUT"][i]))
        ev_df_dict["CONTROLLER_ID"].append(into_id(ev_df_dict["CONTROLLER"][i]))
    
    # Catches when EVENT_ID is an output.
    except IndexError:
        anomalies.append(i)
        ev_df_dict["OUTPUT_ID"].append(ev_df_dict["OUTPUT"][i])
        ev_df_dict["CONTROLLER_ID"].append(ev_df_dict["CONTROLLER"][i])
        continue
        
# Converts lists into ordered pandas series object
ev_df_dict["OUTPUT_ID"] = pd.Series(ev_df_dict["OUTPUT_ID"])
ev_df_dict["CONTROLLER_ID"] = pd.Series(ev_df_dict["CONTROLLER_ID"])

# Convert to dataframe...
ev_id_df = pd.DataFrame.from_dict(ev_df_dict)
ev_id_df = ev_id_df.drop_duplicates(subset=["OUTPUT_ID", "CONTROLLER_ID", "SEEN_IN"]).reset_index(drop=True)
ev_id_df = ev_id_df.astype(str)

# ... to save as a csv file.
ev_id_df.to_csv("AllActNC.csv", index=False)
