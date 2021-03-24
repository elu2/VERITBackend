import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
import csv
import math

#Read the csv file into a networkx graph object
g = nx.read_edgelist("query_edges_fixed.txt", create_using=nx.DiGraph, delimiter=",", nodetype=str, data=(("weight",int),("color_col",float),("penwidth",int)))


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
with open("query_nodes_fixed.txt","r") as infile:
    reader=csv.reader(infile)
    node_names={row[1]:row[0] for row in reader}

#Add node labels
for n in g.nodes():
    g.nodes[n]["label"]=node_names[n]


#Write g to dot file
out_file_name="reach_subset.dot"
write_dot(g,"reach_subset.dot") 

#Get dimensions
n_nodes=len(list(g.nodes()))
dims=n_nodes+8
dims=str(dims)+","+str(dims)
                    
#Create visualization
os.system("dot -Goverlap=false -Nstyle=filled -Nfontcolor=black -Goutputorder=edgesfirst -Gsize="+dims+"\! -Gbgcolor=black -Tpng "+out_file_name+" -O")
