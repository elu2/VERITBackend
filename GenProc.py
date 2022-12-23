import pandas as pd
import networkx as nx
import numpy as np
import datetime
import pickle
import os


# Preprocessing concatenated papers by removing anomalies and separating id from name
def preproc(df):
    # Strings that we do not want to see in OUTPUT and CONTROLLER
    offenders = [":", "{", "[", "::uberon:UBERON:", "::cl:CL:", "ice::uniprot:P41944", "ass::go:GO:0016049"]
    comb_ser = df["OUTPUT"] + df["CONTROLLER"]
    
    drop_rows = comb_ser.str.contains("|".join(offenders), regex=False) == False
    drop_rows = (df["OUTPUT"].str.contains("(.*::.*::.*)|(.*::(\..){0,1}$)") == False) * drop_rows
    drop_rows = (df["OUTPUT"].str.contains(":") == True) * drop_rows
    drop_rows = (df["CONTROLLER"].str.contains("(.*::.*::.*)|(.*::(\..){0,1}$)") == False) * drop_rows

    df = df[drop_rows].reset_index(drop=True)

    # Remove suffixes
    suff_rows = df["OUTPUT"].str.contains(".*\..{1}$")
    df["OUTPUT"][suff_rows] = df["OUTPUT"][suff_rows].str[:-2]
    suff_rows = df["CONTROLLER"].str.contains(".*\..{1}$")
    df["CONTROLLER"][suff_rows] = df["CONTROLLER"][suff_rows].str[:-2]

    # Split output and controller into their common name and ids
    # Some databases redundantly repeat their name in the id
    output_ids = df["OUTPUT"].str.split("::", expand=True, regex=False).rename(columns={0:"OUTPUT NAME", 1:"OUTPUT ID"})
    output_ids["OUTPUT ID"] = output_ids["OUTPUT ID"].str.split(":", regex=False).apply(lambda x: f"{x[-2]}:{x[-1]}")
    anom_rows = output_ids["OUTPUT ID"].str.contains(".", regex=False)
    output_ids["OUTPUT ID"][anom_rows] = output_ids["OUTPUT ID"][anom_rows].str.split(".", regex=False).apply(lambda x: x[0])

    contro_ids = df["CONTROLLER"].str.split("::", expand=True, regex=False).rename(columns={0:"CONTROLLER NAME", 1:"CONTROLLER ID"})
    contro_ids["CONTROLLER ID"] = contro_ids["CONTROLLER ID"].str.split(":", regex=False).apply(lambda x: f"{x[-2]}:{x[-1]}")
    anom_rows = contro_ids["CONTROLLER ID"].str.contains(".", regex=False)
    contro_ids["CONTROLLER ID"][anom_rows] = contro_ids["CONTROLLER ID"][anom_rows].str.split(".", regex=False).apply(lambda x: x[0])

    df = pd.concat([output_ids, contro_ids, df], axis=1)

    return df


# Concatenate evidence by interaction pair. Does not include low-occurrence interactions
def concat_ev(evidence_df, drop_degree=1):
    # Remove interactions with low occurrences
    count_df = evidence_df.groupby(["OUTPUT ID", "CONTROLLER ID"]).size().reset_index().rename(columns={0: "TOT COUNTER"})
    count_df = count_df[count_df["TOT COUNTER"] > drop_degree].reset_index(drop=True)
    evidence_df = count_df.merge(evidence_df, on=["OUTPUT ID", "CONTROLLER ID"]).drop("TOT COUNTER", axis=1)

    # Add separators to labels and PMCIDs for later
    evidence_df["EVENT LABEL"] = evidence_df["EVENT LABEL"].apply(lambda x: f"|{x}|")
    evidence_df["SEEN IN"] = evidence_df["SEEN IN"].apply(lambda x: f"({x})")
    
    # Join evidence, id, and label into one
    evidence_df["EVIDENCE"] = evidence_df[["EVIDENCE", "SEEN IN", "EVENT LABEL"]].agg(" ".join, axis=1)

    # Join all processed evidence by interaction pair
    evidence_df = evidence_df.groupby(["OUTPUT ID","CONTROLLER ID"])["EVIDENCE"].apply("%%".join).reset_index()

    evidence_df.columns = ["target", "source", "evidence"]

    return evidence_df


# Counts interactions and create confidence values for each interaction type
def get_edges(df, drop_degree=1):
    # Count occurences of interactions
    counted = df.groupby(by=["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL"]).size()
    counted = pd.DataFrame(counted).reset_index().rename(columns={0: "COUNTER"})
    df = df.merge(counted, on=["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL"])
    
    # Sum together all occurences of interaction
    inter_tts = counted.groupby(["OUTPUT ID", "CONTROLLER ID"])["COUNTER"].sum().reset_index()
    
    event_pivot = counted.pivot(index=["OUTPUT ID", "CONTROLLER ID"], columns="EVENT LABEL", values="COUNTER").reset_index()

    event_props = inter_tts.merge(event_pivot, on=["OUTPUT ID", "CONTROLLER ID"]).fillna(0)

    event_props["CONF"] = (event_props["Activation (Positive)"] - event_props["Activation (Negative)"]) / event_props["COUNTER"]
    
    event_props = event_props.drop(columns=["Activation (Positive)", "Activation (Negative)", "Inconclusive"])

    if drop_degree > 0:
        event_props = event_props[event_props["COUNTER"] > drop_degree]
    
    return event_props


# Get all encountered IDs and names
def get_nodes(df):
    # Stack relevant columns and drop duplicates
    outputs = full_df[["OUTPUT NAME", "OUTPUT ID"]]
    outputs.columns = ["Label", "Id"]
    
    controllers = full_df[["CONTROLLER NAME", "CONTROLLER ID"]]
    controllers.columns = ["Label", "Id"]

    nodes = pd.concat([outputs, controllers]).drop_duplicates()
    
    return nodes


# Normalization function for pagerank values. Subject to change.
def normalize(vals):
    vals = np.log(vals)
    
    maxv = max(vals)
    minv = min(vals)
    
    normed = (vals - minv) / (maxv - minv)
    
    return normed


# Assigns each node a normalized pagerank value
def pagerank_nodes(nodes, edges):
    G = nx.from_pandas_edgelist(edges, "source", "target", edge_attr="thickness")
    pr_dict = nx.pagerank(G, weight="thickness")
    pr_df = pd.DataFrame(pd.Series(pr_dict)).reset_index()

    pr_df.columns = ["Id", "PR"]
    pr_df["PR"] = normalize(pr_df["PR"])
    
    nodes = nodes.merge(pr_df, on="Id")
    
    return nodes


if __name__ == "__main__":
    # Read in and combine the two (new) important csv files.
    new_act_df = pd.read_csv('NewAllAct.csv', encoding='utf-8')
    new_nc_df = pd.read_csv("NewAllNC.csv", encoding='utf-8')
    
    new_full_df = pd.concat([new_act_df, new_nc_df], ignore_index=True); del new_act_df; del new_nc_df
    new_full_df = new_full_df.drop(columns="INPUT")
    # Preprocess only the new files (bottleneck)
    new_full_df = preproc(new_full_df)
    
    # Read in old and combine new and (preprocessed) old
    if os.path.exists("./AllActNC.csv"):
        old_act_nc_df = pd.read_csv('AllActNC.csv', encoding='utf-8')
        full_df = pd.concat([old_act_nc_df, new_full_df], ignore_index=True); del old_act_nc_df; del new_full_df
    else:
        full_df = new_full_df; del new_full_df

    # Process and push evidence into its separate file
    evidence = full_df[["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL", "EVIDENCE", "SEEN IN"]]
    evidence = concat_ev(evidence)
    evidence.to_csv("evidence.csv", index=False)
    full_df.drop(columns="EVIDENCE")
    del evidence

    # Write out for record-keeping
    full_df.to_csv("AllActNC.csv", index=False)

    # Get confidence of interaction IDs and write as edges
    # drop_degree: drop interactions with below-threshold occurrences
    edges = get_edges(full_df, drop_degree=1)
    edges.columns = ["target", "source", "thickness", "color"]
    edges.to_csv("edges.csv", index=False)

    # Get nodes
    nodes = get_nodes(full_df)
    nodes = pagerank_nodes(nodes, edges)
    nodes.to_csv("nodes.csv", index=False)
    
    # Remove new files created by NCEvProc and ActEvProc
    os.remove("./NewAllAct.csv")
    os.remove("./NewAllNC.csv")
    
    # Update logs
    # Read in old files used
    if os.path.exists("./pat.log.pkl"):
        with open('pat.log.pkl', 'rb') as f:
            prev_pat = pickle.load(f)
    else:
        prev_pat = []
    # Read in newly processed
    with open('torun.log.pkl', 'rb') as f:
        to_run = pickle.load(f)
    # Combine and write out new
    prev_pat.extend(to_run)
    with open('pat.log.pkl', 'wb') as f:
        prev_pat = [x for x in prev_pat if "PMC" in x]
        pickle.dump(prev_pat, f)

    with open("runs.log", "a") as f:
        time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"{time_now} (GenProc.py) Finished.\n")
