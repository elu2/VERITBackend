import pandas as pd

evidence = pd.read_csv("evidence.csv", encoding="utf-8")
nodes = pd.read_csv("nodes.csv", encoding="utf-8")
edges = pd.read_csv("edges.csv", encoding="utf-8")

evidence.to_pickle("evidence.pkl")
nodes.to_pickle("nodes.pkl")
edges.to_pickle("edges.pkl")
