#!/usr/bin/env python
# coding: utf-8

# Note: write_dot throws error when node name begins with % sign
# Some nodes begin with a % sign instead of their correct name (REACH error I think)
# Grep for any % signs, and manually replace any with the name corresponding to the id
# 
# Also, save the csv file as UTF 8 csv on excel before importing
# 
# edgelist should be in format source,target,edge_attributes (remove any source/target attribute columns)
# 
# Rename csv file to .txt file, then delete the column names (makes it easier to work with)

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
import csv

#Read the csv file into a networkx graph object
g = nx.read_edgelist("edges_fixed.txt", create_using=nx.DiGraph, delimiter=",", nodetype=str, data=(("color_col",float),("weight",int),("penwidth",int)))

#Add edge colorscheme, change to gradients later
for e in g.edges():
    if g.edges[e]["color_col"]<.5:
        g.edges[e]["color"]="blue"
    elif g.edges[e]["color_col"]==.5:
        g.edges[e]["color"]="gray"
    else:
        g.edges[e]["color"]="red"
        
#Make node dictionary, format=node:node_label
node_names={}
with open("nodes.txt","r") as infile:
    reader=csv.reader(infile)
    node_names={row[0]:row[1] for row in reader}

#Add node labels
for n in g.nodes():
    parts=node_names[n].split("::")
    #Format: id (common name)
    g.nodes[n]["label"]=n+" ("+parts[0]+")"
  
#Write g to dot file
out_file_name="reach_subset.dot"
write_dot(g,"reach_subset.dot") 

#Create visualization
os.system("sfdp -Goverlap=prism -Nstyle=filled -Nfontcolor=white -Goutputorder=edgesfirst -Tsvg "+out_file_name+" -O")
os.system("sfdp -Goverlap=prism -Nstyle=filled -Nfontcolor=white -Goutputorder=edgesfirst -Tsvg "+other+" -O")


