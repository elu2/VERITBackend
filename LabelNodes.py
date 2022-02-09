import pandas as pd


def into_two(string):
    split_string = string.split(":")
    split_id = split_string[-2] + ":" + split_string[-1]
    split_name = string.split(":")[0]
    
    if "." in split_id:
        split_id = split_id.split(".")[0]
    
    return split_name, split_id


nodes_table = pd.read_csv("nodes_table_all.csv", encoding="UTF-8")
nodes_table_dict = nodes_table.to_dict()
nodes_table_dict["Label"] = []
nodes_table_dict["Only_Id"] = []

i = 0
for i in range(len(nodes_table_dict["Id"])):
    try:
        name, only_id = into_two(nodes_table_dict["Id"][i])
        nodes_table_dict["Label"].append(name)
        nodes_table_dict["Only_Id"].append(only_id)
    except IndexError:
        name = nodes_table_dict["Id"][i]
        only_id = "NotFound"
        nodes_table_dict["Label"].append(name)
        nodes_table_dict["Only_Id"].append(only_id)
    i += 1

nodes_table_dict["Label"] = pd.Series(nodes_table_dict["Label"])
nodes_table_dict["Only_Id"] = pd.Series(nodes_table_dict["Only_Id"])

nodes_table_all_labelled = pd.DataFrame(nodes_table_dict)

### Part 2: Labelling nodes with Normalized pagerank values

from networkx.algorithms.link_analysis.pagerank_alg import pagerank
import networkx as nx
import numpy as np

edges = pd.read_csv("/xdisk/guangyao/elu2/RV/REACHVisualization/edges_table.csv")
nodes = pd.read_csv("/xdisk/guangyao/elu2/RV/REACHVisualization/nodes_table_all_labelled.csv")


def standardize(x, mu, sigma):
    return (x - mu)/sigma


if nodes.columns[0] == "index":
    nodes = nodes.iloc[:, 1:]
    
graph = nx.from_pandas_edgelist(edges, source="source_id", target="target_id", edge_attr="thickness")
edge_pr = pagerank(graph, weight="thickness")

pr_df = {
    "Only_Id": edge_pr.keys(),
    "pagerank": edge_pr.values()
}

mu = np.mean(list(pr_df["pagerank"]))
sigma = np.std(list(pr_df["pagerank"]))

pr_df = pd.DataFrame(pr_df)
pr_df["PRValue"] = pr_df["pagerank"].apply(standardize, args=(float(mu), float(sigma)))

new_nodes = pd.merge(nodes, pr_df[["Only_Id", "PRValue"]], how="outer", on="Only_Id")
new_nodes.to_csv("nodes_table_all_labelled.csv", index=False)

nodes_table_all_labelled.to_csv("nodes_table_all_labelled.csv", index=False)
