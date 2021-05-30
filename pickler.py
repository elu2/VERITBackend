import pandas as pd
import pickle

evidence_pd = pd.read_csv("evidence.csv", encoding="utf-8")
nodes_pd = pd.read_csv("nodes_table_all_labelled.csv", encoding="utf-8")
edges_pd = pd.read_csv("edges_table.csv", encoding="utf-8")

pickle.dump(evidence_pd, open("evidence.pkl", "wb"))
pickle.dump(nodes_pd, open("nodes_table_all_labelled.pkl", "wb"))
pickle.dump(edges_pd, open("edges_table.pkl", "wb"))
