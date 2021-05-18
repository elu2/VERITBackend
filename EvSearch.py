import pandas as pd

# The edges table to find evidence from. Reads "source" and "target" columns which must each contain only IDs.
input_edges = "query_edges.csv"


def get_evidence(edges_table_df, ev_id_df):
    edges_id_cols = edges_table_df[["source", "target"]]
    edges_id_dict = edges_id_cols.to_dict()
    edges_id_dict["LONG_EVIDENCE"] = []

    # len(edges_id_dict["source_id"])
    for i in range(len(edges_id_dict["source"])):
        # Finds the single pair's matches in the evidence dataframe (SLOW)
        out_id = id_subset_dict["OUTPUT_ID"][i]
        cont_id = id_subset_dict["CONTROLLER_ID"][i]
        query_ev = ev_id_df.query('(OUTPUT_ID==@out_id) & (CONTROLLER_ID==@cont_id)').reset_index(drop=True)
        
        # Creates a long string of all evidence
        evidence_concat = str()
        j = 0
        for j in range(len(query_ev["OUTPUT_ID"])):
            evidence_concat += query_ev["EVIDENCE"][j] + "[" + query_ev["EVENT_LABEL"][j] + "] "

        # Adds the entire concatenated string as a column's entry
        edges_id_dict["LONG_EVIDENCE"].append(evidence_concat)

    edges_id_dict["LONG_EVIDENCE"] = pd.Series(edges_id_dict["LONG_EVIDENCE"])
    edges_ev_df = pd.DataFrame(edges_id_dict)

    return edges_ev_df


edges_table_df = pd.read_csv(input_edges)
ev_id_df = pd.read_csv("ev_id.csv")
get_evidence(edges_table_df, ev_id_df).to_csv("query_ev.csv")
