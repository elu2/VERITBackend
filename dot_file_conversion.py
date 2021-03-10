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


#Read the csv file into a networkx graph object

g = nx.read_edgelist("subset_query_edges.txt", create_using=nx.DiGraph, delimiter=",", nodetype=str, data=(("color_col",float),("weight",int),("thickness",int)))


write_dot(g,"reach_subset.dot")

