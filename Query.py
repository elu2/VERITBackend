#!/usr/bin/env python
# coding: utf-8

import itertools as it
import pandas as pd
import csv
import math
import numpy as np


# Function to find the shortest path between two nodes of a graph 
def BFS_SP(graph, start, goal): 
    explored = [] 
      
    # Queue for traversing the graph in the BFS 
    queue = [[start]] 
      
    # If the desired node is reached 
    if start == goal: 
        print("Same Node") 
        return
      
    # Loop to traverse the graph with the help of the queue 
    while queue: 
        path = queue.pop(0) 
        node = path[-1] 
          
        # Codition to check if the current node is not visited 
        if node not in explored: 
            neighbours = graph[node] 
              
            # Loop to iterate over the neighbours of the node 
            for neighbour in neighbours: 
                new_path = list(path) 
                new_path.append(neighbour) 
                queue.append(new_path) 
                  
                # Condition to check if the neighbour node is the goal 
                if neighbour == goal: 
                    print(f"Shortest path for ({start}) --> ({goal}) = ", [*new_path])
                    return new_path
            explored.append(node) 
  
    # Condition when the nodes are not connected 
    print("No path.") 
    return


# Make a dictionary for all nodes and their connections.
edges_table = pd.read_csv("edges_table.csv", encoding="latin-1")
sources = edges_table["source_id"].tolist()
targets = edges_table["target_id"].tolist()
sources_label = edges_table["source"].tolist()
targets_label = edges_table["target"].tolist()
color_col = edges_table["color_col"].tolist()
weight = edges_table["weight"].tolist()
thickness = edges_table["thickness"].tolist()

all_species = list(set(sources + targets))

# Initialize a graph dictionary. A key is made for every species. The ones that appear as a source has its target appended to the value.
i = 0
graph_dict = {}
for i in range(0, len(all_species)):
    graph_dict[all_species[i]] = []

for i in range(0, len(sources)):
    graph_dict[sources[i]].append(targets[i])

all_species_id = []
i=0
for species in all_species:
    if len(species) > 8:
        all_species_id.append(species.split(":")[-2] + ":" + species.split(":")[-1])
    else:
        all_species_id.append(species)


# nCr where n is the number of inputs, r is 2 for pairing.
# the txt file will need to take IDs only. This means we'll have to search the table for the IDs and convert them into full labels.

queries_id = []

with open("query_list.txt", 'r', encoding="UTF-8") as query_list:
    queries_id = query_list.readlines()

queries_id = [line.strip() for line in queries_id]

output_num = math.factorial(len(queries_id))/(2*math.factorial((len(queries_id) - 2)))

q_combinations = it.combinations(queries_id, 2)


queries = []
for query in queries_id:
    i = 0
    for species_id in all_species_id:
        if query == species_id:
            queries.append(all_species[i])
        i += 1


print(f"Printed {output_num} Source, Target pairs.")

stored_paths = {}
for query_pair in q_combinations:
    source, target = query_pair
    stored_paths[f"{source} -> {target}"] = BFS_SP(graph_dict, source, target)


expanded_paths = {}
for key in stored_paths:
    breakdown_list = stored_paths[key]
    if breakdown_list != None:
        sub_pairings = []
        for i in range(0, len(breakdown_list) - 1):
            sub_pairings.append(tuple([breakdown_list[i], breakdown_list[i + 1]]))
        expanded_paths[key] = sub_pairings
    if breakdown_list == None:
        expanded_paths[key] = None


subsetted_edges = {
    "source" : [],
    "target" : [],
    "source_label" : [],
    "target_label" : [],
    "color_col" : [],
    "weight" : [],
    "thickness" : []
}

pathless_pairs = []

for key in expanded_paths:
    if expanded_paths[key] != None:
        for pair in expanded_paths[key]:
            i = 0
            for i in range(0, len(sources)):
                if sources[i] == pair[0] and targets[i] == pair[1]:
                    subsetted_edges["source"].append(sources[i])
                    subsetted_edges["target"].append(targets[i])
                    subsetted_edges["source_label"].append(sources_label[i])
                    subsetted_edges["target_label"].append(targets_label[i])
                    subsetted_edges["color_col"].append(color_col[i])
                    subsetted_edges["weight"].append(weight[i])
                    subsetted_edges["thickness"].append(thickness[i])
    else:
        pathless_pairs.append(key)


query_edges = pd.DataFrame.from_dict(subsetted_edges)
no_dupes = pd.DataFrame(np.sort(query_edges[['source','target']], axis=1))
query_edges = query_edges[~no_dupes.duplicated()]

# Dictionary to easily reference a node id to their common name

all_nodes_table = pd.read_csv("nodes_table_all_labelled.csv", encoding="latin-1")
node_names = all_nodes_table["Id"]
node_labels = all_nodes_table["Label"]
labels_dict = {}

for i in range(0, len(node_names)):
    if len(node_names[i]) > 8:
        node_id_split = node_names[i].split(":")
        node_id = node_id_split[-2] + ":" + node_id_split[-1]
        labels_dict[node_id] = node_labels[i]
    else:
        labels_dict[node_names[i]] = node_labels[i]


im_combined_nodes = subsetted_edges["source"] + subsetted_edges["target"]
query_nodes_im = {"Id" : list(set(im_combined_nodes))}
query_nodes = pd.DataFrame.from_dict(query_nodes_im)

query_nodes_labels = {"Label" : []}
for node_im_id in query_nodes_im["Id"]:
    query_nodes_labels["Label"].append(labels_dict[node_im_id])


query_nodes_labels_df = pd.DataFrame.from_dict(query_nodes_labels)
labelled_query_nodes = pd.concat([query_nodes, query_nodes_labels_df], axis=1)


labelled_query_nodes.to_csv("query_nodes.csv", index=False)
query_edges.to_csv("query_edges.csv", index=False)
