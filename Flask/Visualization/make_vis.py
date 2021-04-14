import pandas as pd
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
import csv
import math
import time

def make_vis(outfile):
    nodes_df=pd.read_csv("query_nodes.csv",header = 0)
    edges_df=pd.read_csv("query_edges.csv",header = 0)
    edges_df=edges_df.drop(columns=["source_lab", "target_lab"])
    nodes_df=nodes_df.drop(columns=["FullName"])


    #remove commas
    nodes_df["Id"]=nodes_df["Id"].str.replace(",","")
    nodes_df["Label"]=nodes_df["Label"].str.replace(",","")
    edges_df["source"]=edges_df["source"].str.replace(",","")
    edges_df["target"]=edges_df["target"].str.replace(",","")

    #replace weight column with thickness column
    edges_df["weight"] = edges_df["thickness"]

    #Take square root of thickness column so the edges aren't too big for the large values
    edges_df["thickness"]=np.sqrt(edges_df["thickness"])
    edges_df["thickness"] = edges_df["thickness"].astype(int)

    edges_df.to_csv("query_edges_fixed.csv", index=False, header=False, encoding='ascii', errors='ignore')
    nodes_df.to_csv("query_nodes_fixed.csv", index=False, header=False, encoding='ascii', errors='ignore')

    #Read the csv file into a networkx graph object
    g = nx.read_edgelist("query_edges_fixed.csv", create_using=nx.DiGraph, delimiter=",", nodetype=str, data=(("weight",int),("color_col",float),("penwidth",int)))


    #Add edge colors
    for e in g.edges():
        g.edges[e]["colorscheme"]="rdylbu9"
        if g.edges[e]["color_col"]==1:
            g.edges[e]["color"]=1
        elif g.edges[e]["color_col"]<.1:
            g.edges[e]["color"]=9
        else:
            g.edges[e]["color"]=10-math.floor(g.edges[e]["color_col"]*10)

    #Make node dictionary, format=node:node_label
    node_names={}
    with open("query_nodes_fixed.csv","r") as infile:
        reader=csv.reader(infile)
        node_names={row[1]:row[0] for row in reader}

    #Add node labels
    for n in g.nodes():
        g.nodes[n]["label"]=node_names[n]



    #Remove previous images in static/
    for filename in os.listdir('static/'):
        if filename.startswith('reach_subset'):  # not to remove other images
            os.remove('static/' + filename)
            
    
            

            
    #Write g to dot file
    write_dot(g,outfile) 

    #Get dimensions
    n_nodes=len(list(g.nodes()))
    dims=n_nodes+8
    dims=str(dims)+","+str(dims)
    

    #Create visualization
    os.system("dot -Goverlap=false -Nstyle=filled -Nfontcolor=black -Goutputorder=edgesfirst -Gsize="+dims+"\! -Gbgcolor=black -Tpng "+outfile+" -O")
    
    os.system("mv "+outfile+".png static/")
    
    #Remove the dot file
    os.system("rm -rf reach_subset*")



