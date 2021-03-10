#!/usr/bin/env python
# coding: utf-8

# Updating nodes to include label
import pandas as pd
import csv

file_name = "nodes_table_all.csv"
node_labels = []
with open(file_name, "r") as nodes_table:
    reader = nodes_table.readlines()
    for row in reader[1:]:
        node_labels.append(row.split("::")[0][1:])
        
nodes_table = pd.read_csv(file_name, encoding='latin-1')
nodes_table["label"] = nodes_table["Id"]
del nodes_table['label']
nodes_table["Label"] = node_labels 

nodes_table.to_csv("nodes_table_all_labelled.csv")
