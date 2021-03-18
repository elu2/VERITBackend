#!/usr/bin/env python
# coding: utf-8

# Updating nodes to include label
import pandas as pd
import csv

file_name = "nodes_table_all.csv"
node_labels = []
reader_s = []
only_ids = []
with open(file_name, "r", encoding="UTF-8") as nodes_table:
    reader = nodes_table.readlines()
    for row in reader[1:]:
        if len(row) > 8:
            reader_s.append(row.strip('"')[:-2])
            node_labels.append(row.split("::")[0][1:])
            only_ids.append(row.split(":")[-2] + ":" + row.split(":")[-1][:-2])
        else:
            reader_s.append(row.strip('"')[:-2])
            node_labels.append(row.split("::")[0][1:-2])
            only_ids.append(row.split("::")[0][1:-2])

labelled_dict = {
    "Id" : reader_s,
    "Label": node_labels,
    "Only_Id": only_ids
}

labelled_df = pd.DataFrame.from_dict(labelled_dict)

labelled_df.to_csv("nodes_table_all_labelled.csv")
