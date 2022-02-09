from networkx.algorithms.link_analysis.pagerank_alg import pagerank
import networkx as nx
import pandas as pd
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
