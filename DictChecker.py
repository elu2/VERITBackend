#!/usr/bin/env python
# coding: utf-8

import pandas as pd


edges_table = pd.read_csv("edges_table.csv", encoding="latin-1")
sources = edges_table["source_id"].tolist()
targets = edges_table["target_id"].tolist()
color_col = edges_table["color_col"].tolist()

all_species = list(set(sources + targets))

queries_id = []
with open("query_list.txt", 'r', encoding="UTF-8") as query_list:
    queries_id = query_list.readlines()

print(f"Reading {len(queries_id)} queries.")

queries_id = [line.strip() for line in queries_id]

all_in = True
not_in_counter = 0
for query in queries_id:
    if query not in all_species:
        print(f"{query} not in network.")
        all_in = False
        not_in_counter += 1
    else:
        continue

if all_in == True:
    print("All queries in network.")
else:
    print(f"{not_in_counter}/{len(queries_id)} species out of network.")
