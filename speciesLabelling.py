# This script is not very user-friendly. Uncomment the bigBatch.txt creation portion, 
# then use the link to query directly from UniProt,
# then comment out the the creation portion again and rerun.

import pandas as pd
import numpy as np
import os
import pickle


def includes_pubchem(string):
    if "uniprot" in string:
        return string[8:]


def batch_dict_constructor(uniprot_from, batch_n):
    # split into batches of 10000
    batches = {}
    full_batches = len(uniprot_from)//batch_n
    for i in range(full_batches):
        batches[i] = uniprot_from[i * batch_n: (i + 1) * batch_n]
        batches[i]= [x.strip("{}") for x in batches[i]]
    
    # remainder of ids
    batches[full_batches] = uniprot_from[full_batches * batch_n:]
    
    return batches


def query_constructor(batch):
    full_query = ""
    
    for from_id in batch:
        full_query += from_id + " "
    full_query = full_query[:-1]
    
    return full_query


def DDR(df):
    df = df.drop(columns=["Entry", "Organism", "UniProt"])
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df = df.replace(np.nan, "dne")
    return df
  
 
table = pd.read_csv("nodes_table_all_labelled.csv", encoding="utf-8")    
nid = table["Only_Id"].apply(includes_pubchem)
uniprot_from = nid.dropna()
table["UniProt"] = nid

# Option to make and write out separate batches
'''
batch_dict = batch_dict_constructor(uniprot_from, 30000)

for batch in batch_dict.keys():
    batch_dict[batch] = query_constructor(batch_dict[batch])
    
for batch in batch_dict.keys():
    with open(f'batches/{batch}.txt', "w") as file:
        file.write(batch_dict[batch])
'''

# Or just 1 big batch to copy and paste
# Manual labor: use https://www.uniprot.org/uploadlists/ to get relevant columns
# Duplicates will be found; run another using the duplicates
'''
with open("batches/bigBatch.txt", "w") as file:
    file.write(query_constructor(list(uniprot_from)))
'''

if not os.path.exists("./batches/"):
    os.mkdir("./batches/")
    print("Created batches/ directory.")

# Then stick the two dataframes together
df1 = pd.read_csv("batches/Full_1.tab", sep="\t", encoding="utf-8")
df2 = pd.read_csv("batches/Full_2.tab", sep="\t", encoding="utf-8")

df = pd.concat([df1, df2])

# Merge and process
with_species = pd.merge(table, df, left_on="UniProt", right_on="Entry", how="left")
with_species = DDR(with_species)

# Overwrite Label column with UniProt IDs
en_al = list(with_species["Entry name"])
l_al = list(with_species["Label"])
final_label = []
for label, entry_name in zip(l_al, en_al):
    if entry_name == "dne":
        final_label.append(label)
    else:
        final_label.append(entry_name)
    
table["Label"] = final_label
table = table.drop("UniProt", axis=1)

pickle.dump(table, open("nodes_table_all_labelled.pkl", "wb"))
