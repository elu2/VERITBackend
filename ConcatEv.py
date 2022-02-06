import pandas as pd

edges_df=pd.read_csv("edges_table.csv")
nodes_df=pd.read_csv("nodes_table_all_labelled.csv")
all_df=pd.read_csv("AllActNC.csv")

#Add pipe separators to the event labels
def add_pipe(string):
    return "|"+string+"|"

all_df["EVENT_LABEL"]=all_df["EVENT_LABEL"].apply(add_pipe)

#Add parentheses to the PMCIDs
def add_parentheses(string):
    return "("+string+")"
all_df["SEEN_IN"]=all_df["SEEN_IN"].apply(add_parentheses)


#Make another column with concatenated EVIDENCE and PMCID
all_df["EVIDENCE2"]=all_df["EVIDENCE"].str.cat(all_df["SEEN_IN"], sep=" ")

#Make another column with concatenated evidence, PMCID, and event label
all_df["EVIDENCE2"]=all_df["EVIDENCE2"].str.cat(all_df["EVENT_LABEL"], sep="")

#Replace original evidence column with the concatenated column
all_df["EVIDENCE"]=all_df["EVIDENCE2"]

#Drop all columns except OUTPUT_ID, CONTROLLER_ID, and EVIDENCE
all_df=all_df.drop(labels=["INPUT","OUTPUT","CONTROLLER","EVENT_ID","EVENT_LABEL","EVIDENCE2","SEEN_IN"], axis=1)

#Group rows with same OUTPUT_ID and CONTROLLER_ID together, concatenate their evidences with %% separator
all_df=all_df.groupby(["OUTPUT_ID","CONTROLLER_ID"])["EVIDENCE"].apply("%%".join).reset_index()

#Rename columns to be the same as edges_table.csv
all_df.columns=["target_id","source_id","evidence"]

#Join edges_table with all_df, so that we have color and thickness of the edges
edges_df_ev=pd.merge(edges_df, all_df, how="inner", on=["source_id", "target_id"])[["source","source_id","target","target_id","color_col","thickness","evidence"]]

#Write new tables to csv
ev_table=edges_df_ev.drop(labels=["source","target","color_col","thickness"], axis=1)
edges_df=edges_df_ev.drop(labels=["evidence"], axis=1)

ev_table.to_csv("evidence.csv",index=False)
edges_df.to_csv("edges_table.csv", index=False)
