import pandas as pd
import networkx as nx
import numpy as np


def preproc(df):
    # Handle when output is an event id
    drop_rows = df["OUTPUT"].str.contains(":", regex=False)
    drop_rows = (df["OUTPUT"].str.contains("(.*::.*::.*)|(.*::(\..){0,1}$)") == False) * drop_rows
    drop_rows = (df["OUTPUT"].str.contains("{", regex=False) == False) * drop_rows

    drop_rows = (df["CONTROLLER"].str.contains(":", regex=False) == True) * drop_rows
    drop_rows = (df["CONTROLLER"].str.contains("(.*::.*::.*)|(.*::(\..){0,1}$)") == False) * drop_rows
    drop_rows = (df["CONTROLLER"].str.contains("{", regex=False) == False) * drop_rows
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


def concat_ev(evidence_df):
    evidence_df["EVENT LABEL"] = evidence_df["EVENT LABEL"].apply(lambda x: f"|{x}|")
    evidence_df["SEEN IN"] = evidence_df["SEEN IN"].apply(lambda x: f"({x})")
    
    evidence_df["EVIDENCE"] = evidence_df[["EVIDENCE", "SEEN IN", "EVENT LABEL"]].agg(" ".join, axis=1)

    evidence_df = evidence_df.groupby(["OUTPUT ID","CONTROLLER ID"])["EVIDENCE"].apply("%%".join).reset_index()

    evidence_df.columns = ["target", "source","evidence"]

    return evidence_df


def get_edges(df, drop_degree=1):
    # Count occurences of interactions
    counted = df.groupby(by=["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL"]).size()
    counted = pd.DataFrame(counted).reset_index().rename(columns={0: "COUNTER"})
    df = df.merge(counted, on=["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL"])
    
    # Sum together occurences of event-dependent interactions
    inter_cts = df.groupby(["OUTPUT ID", "CONTROLLER ID", "EVENT LABEL"])["COUNTER"].sum().reset_index()
    # Sum together all occurences of interaction
    inter_tts = inter_cts.groupby(["OUTPUT ID", "CONTROLLER ID"])["COUNTER"].sum().reset_index()
    

    event_pivot = inter_cts.pivot(index=["OUTPUT ID", "CONTROLLER ID"], columns="EVENT LABEL", values="COUNTER").reset_index()

    event_props = inter_tts.merge(event_pivot, on=["OUTPUT ID", "CONTROLLER ID"])

    event_props["Activation (Negative)"] = event_props["Activation (Negative)"] / event_props["COUNTER"]
    event_props["Activation (Positive)"] = event_props["Activation (Positive)"] / event_props["COUNTER"]
    event_props["Inconclusive"] = event_props["Inconclusive"] / event_props["COUNTER"]

    event_props = event_props.fillna(0)
    
    if drop_degree > 0:
        event_props = event_props[event_props["COUNTER"] > drop_degree]
    
    return event_props


def get_nodes(df):
    # Stack relevant columns and drop duplicates
    outputs = full_df[["OUTPUT NAME", "OUTPUT ID"]]
    outputs.columns = ["Label", "Id"]
    
    controllers = full_df[["CONTROLLER NAME", "CONTROLLER ID"]]
    controllers.columns = ["Label", "Id"]

    nodes = pd.concat([outputs, controllers]).drop_duplicates()
    
    return nodes


def pagerank_nodes(nodes, edges):
    G = nx.from_pandas_edgelist(edges, "source", "target", edge_attr="thickness")
    pr_dict = nx.pagerank(G, weight="thickness")
    pr_df = pd.DataFrame(pd.Series(pr_dict)).reset_index()

    pr_df.columns = ["Id", "PR"]
    pr_df["PR"] = (pr_df["PR"] - np.mean(pr_df["PR"]))/np.std(pr_df["PR"])
    
    nodes = nodes.merge(pr_df, on="Id", how="left")
    
    return nodes


if __name__ == "__main__":
    # Read in and combine the two important csv files.
    act_df = pd.read_csv('AllAct.csv', encoding='utf-8')
    nc_df = pd.read_csv("AllNC.csv", encoding='utf-8')

    full_df = pd.concat([act_df, nc_df], ignore_index=True); del act_df; del nc_df
    full_df = full_df.drop(columns="INPUT") 

    full_df = preproc(full_df)

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
    edges.columns = ["target", "source", "thickness", "neg_color", "pos_color", "inc_color"]
    edges.to_csv("edges.csv", index=False)
    
    # Get nodes
    nodes = get_nodes(full_df)
    nodes = pagerank_nodes(nodes, edges)
    nodes.to_csv("nodes.csv", index=False)    
