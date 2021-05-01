import json
import pandas as pd
import numpy as np
import os
import csv
import math

def clean_nodes():

    nodes_df=pd.read_csv("query_nodes.csv",header = 0)

    #Duplicate the depth column in nodes table
    nodes_df["rank"]=nodes_df["depth"]

    #Convert rank values so small values are large and vice versa
    def get_rank_value(rank):
        if rank==0:
            return 1000
        elif rank==1:
            return 600
        elif rank==2:
            return 400
        elif rank==3:
            return 200
        elif rank==4:
            return 0

    nodes_df["rank"]=nodes_df["rank"].apply(get_rank_value)


    #Convert depth to color in nodes table
    def get_node_color(depth):
        if depth==0:
            return "#fc0800"
        elif depth==1:
            return "#f1c9f2"
        elif depth==2:
            return "#c9ddf2"
        elif depth==3:
            return "#d7f2c9"
        else:
            return "#f7d4ab"

    nodes_df["depth"]=nodes_df["depth"].apply(get_node_color)

    return nodes_df

def clean_edges():
     
    edges_df=pd.read_csv("query_edges.csv",header = 0)

    #Take square root of thickness column so values aren't too big
    edges_df["thickness"]=5*np.sqrt(edges_df["thickness"])

    #Convert the color col into hex color strings
    def get_color(color_val):
        if color_val<.1:
            return "#0560fc"
        elif color_val<.2:
            return "#0589fc"
        elif color_val<.3:
            return "#05bafc"
        elif color_val<.4:
            return "#05fcf8"
        elif color_val<.5:
            return "#fcec05"
        elif color_val<.6:
            return "#fcc205"
        elif color_val<.7:
            return "#fca605"
        elif color_val<.8:
            return "#fc8105"
        elif color_val<.9:
            return "#fc4b05"
        return "#fc0505"

    edges_df["color_col"]=edges_df["color_col"].apply(get_color)

    return edges_df

#Convert nodes and edges tables into one json-style list
def convert(nodes_df, edges_df):
    
    nodes=[]
    for _, row in nodes_df.iterrows():
        parts=row.values.tolist()
        nodes.append(parts)
            
    elements=[]
    for node in nodes:
        node_dict={"data":{"id":node[0], "label":node[1], "color":node[2], "rank":int(node[3])}}
        elements.append(node_dict)
    
    edges=[]
    for _, row in edges_df.iterrows():
        parts=row.values.tolist()
        edges.append(parts)

    for edge in edges:
        edge_id=edge[1]+edge[3]
        edge_dict={"data":{"id":edge_id, "source":edge[1], "target":edge[3], "weight":edge[6], "color":edge[5]}}
        elements.append(edge_dict)

        
    return elements

def clean():
    nodes_df=clean_nodes()
    edges_df=clean_edges()
    return convert(nodes_df, edges_df)
    
        


    
