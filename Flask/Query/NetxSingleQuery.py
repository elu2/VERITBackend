import pandas as pd
import numpy as np
import networkx as nx


def dfs_query(query, depth):
    edges_df = pd.read_csv('edges_table.csv')
    edges_df = edges_df.drop_duplicates(subset=['source_id', 'target_id'], keep="first")
    G = nx.from_pandas_edgelist(edges_df, edge_attr=True, source="source_id", target="target_id", create_using=nx.DiGraph())
   
    T=nx.dfs_tree(G, source=query, depth_limit=depth)
    
    for edge in T.edges:
        T.edges[edge[0], edge[1]]["color_col"]=G.get_edge_data(edge[0],edge[1])['color_col']
        T.edges[edge[0], edge[1]]["thickness"]=G.get_edge_data(edge[0],edge[1])['thickness']
        
    return T

     
def write_out(T, depth, query, thickness_bound):
    
    #Get edges and edge characteristics into a dictionary
    source_ids=[]
    target_ids=[]
    thicknesses=[]
    color_cols=[]
    for edge in T.edges:
        source_ids.append(edge[0])
        target_ids.append(edge[1])
        thicknesses.append(T.edges[edge[0], edge[1]]["thickness"])
        color_cols.append(T.edges[edge[0], edge[1]]["color_col"])
        
    edges_dict={"source_id":source_ids, "target_id":target_ids, "thickness":thicknesses, "color_col":color_cols}
    
    query_edges=pd.DataFrame.from_dict(edges_dict)
    # Drop rows with low literary presence
    query_edges.drop(query_edges[query_edges['thickness'] < thickness_bound].index, inplace = True)
    query_edges.reset_index(drop=True, inplace=True)
    
    query_edges.to_csv("query_edges_unfiltered.csv", index=False)
    
    
    #Dict with depths, and the nodes that were targets at that depth
    depth_ids={0:query}
    sources=[query]
    for i in range(depth):
        depth_ids[i+1]=query_edges[query_edges["source_id"].isin(sources)]["target_id"].tolist()
        sources=depth_ids[i+1]

    def get_depth(node, depth_dict):
        for d in depth_dict:
            if node in depth_dict[d]:
                return d
        return len(depth_dict)-1
            
    source_nodes = query_edges["source_id"].tolist()
    target_nodes = query_edges["target_id"].tolist()
    node_ids = list(set(source_nodes + target_nodes))
    query_nodes = {"Query_Ids": node_ids}
    query_nodes_df = pd.DataFrame.from_dict(query_nodes)
    
    #Get depths for each node
    print(query_nodes_df["Query_Ids"])
    query_nodes_df["depth"]=query_nodes_df["Query_Ids"].apply(get_depth, args=(depth_ids,))

    # Gets the labels for a Query Id.
    nodes_df = pd.read_csv("nodes_table_all_labelled.csv", encoding="UTF-8")
    nodes_df = nodes_df.drop_duplicates(subset='Only_Id', keep="first")
    node_merged_df = pd.merge(nodes_df, query_nodes_df, how="inner", left_on="Only_Id", right_on="Query_Ids")[["Only_Id", "Label", "depth"]]
    node_merged_df.columns = ["Id", "Label", "Depth"]
    
    
    #Write query nodes and edges tables to csv
    node_merged_df.to_csv("query_nodes.csv", index=False)
    query_edges.to_csv("query_edges.csv", index=False)

'''
Query: an id to do dfs query on
depth: an int from 1-4 for the depth to query to
Depth 1 means all immediate connections to query node
'''
    
def query(query, depth, thickness_bound):
    T=dfs_query(query, depth)
    write_out(T, depth, query, thickness_bound)
    
  

        