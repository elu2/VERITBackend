#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import math

df = pd.read_csv("ActLab_df.csv")

# Initialize the dictionary with each key as "INPUT|CONTROLLER|x_a" where x_a is activation type, and value being a list of [num_mentions, pos_or_neg]

interaction_dict = {}
i = 0
for i in range(0, len(df.INPUT)):
    if df.NUM_LABEL[i] == 1:
        interaction_dict[f"{df.INPUT[i]}|{df.CONTROLLER[i]}|pos"] = [df.COUNTER[i], df.NUM_LABEL[i]]
    elif df.NUM_LABEL[i] == -1:
        interaction_dict[f"{df.OUTPUT[i]}|{df.CONTROLLER[i]}|neg"] = [df.COUNTER[i], df.NUM_LABEL[i]]
    i += 1

# We make a proportion dictionary with each key as "Input/Output|Controller" and each value as [pos_count, total_count]

# initialize the dictionary
prop_dict = {}

for key in interaction_dict:
    prop_dict[key[:-4]] = [0, 0]

# Add just Input/Output|Controller as key to prop_dict, and if the activation is postive, add to the first element in the list value. Otherwise
# just add to total.

for key in interaction_dict:
    split_key = key.split("|")
    count = interaction_dict[key][0]
    if split_key[-1] == "pos":
        prop_dict[key[:-4]][0] += count
        prop_dict[key[:-4]][1] += count
    if split_key[-1] == "neg":
        prop_dict[key[:-4]][1] += count

# for each entry in prop_dict, divide pos by total to get the proportion. Then input into the modified tanh function to get our edge value.
# subtract 1 for tanh, leave -1 out for sigmoid

for key in prop_dict:
    proportion = prop_dict[key][0] / prop_dict[key][1]
    y = (1/(1+math.exp(-5*(proportion-.5))))
    prop_dict[key].append(y)

# Change dictionary's form into dataframe-compatible form.
df_dict = {
    "INPUT": [],
    "CONTROLLER": [],
    "EDGE": [],
    "POS": [],
    "TOTAL": [],
}
for key in prop_dict:
    met_input = key.split("|")[-2]
    met_cont = key.split("|")[-1]
    df_dict["INPUT"].append(met_input)
    df_dict["CONTROLLER"].append(met_cont)
    df_dict["EDGE"].append(prop_dict[key][2])
    df_dict["POS"].append(prop_dict[key][0])
    df_dict["TOTAL"].append(prop_dict[key][1])

prop_df = pd.DataFrame.from_dict(df_dict)

i = 0
input_spec = prop_df["INPUT"]
cont_spec = prop_df["CONTROLLER"]
ID_PAIRS = {"ID_PAIRS": []}

# Append input and controller to dictionary as value.
# Conditional on length of the species because only species with char length < 8 will not have a colon to split on.
for i in range(0, len(input_spec)):
    if ":" in input_spec[i]:
        input_spec_id = input_spec[i].split(":")[-2] + ":" + input_spec[i].split(":")[-1]
    if ":" in cont_spec[i]:
        cont_spec_id = cont_spec[i].split(":")[-2] + ":" + cont_spec[i].split(":")[-1]
    else:
        input_spec_id = input_spec[i]
        cont_spec_id = cont_spec[i]

    ID_PAIRS["ID_PAIRS"].append(f"{input_spec_id}|{cont_spec_id}")
    i += 1

ID_PAIRS_df = pd.DataFrame.from_dict(ID_PAIRS)
prop_df = pd.concat([prop_df, ID_PAIRS_df], axis=1, join="inner")
with_id = pd.concat([prop_df["INPUT"], prop_df["CONTROLLER"], ID_PAIRS_df], axis=1, join="inner")
with_id = with_id.drop_duplicates(subset="ID_PAIRS", inplace=False)

unique_dict = {}
for pair in ID_PAIRS_df["ID_PAIRS"]:
    unique_dict[pair] = [0, 0]

i = 0
for i in range(len(prop_df["ID_PAIRS"])):
    id_pair = prop_df["ID_PAIRS"][i]
    unique_dict[id_pair][0] += prop_df["POS"][i]
    unique_dict[id_pair][1] += prop_df["TOTAL"][i]

pos_t_dict = {"POS" : [], "TOTAL": [], "EDGE": []}

for key in unique_dict:
    pos_t_dict["POS"].append(unique_dict[key][0])
    pos_t_dict["TOTAL"].append(unique_dict[key][1])

    proportion = unique_dict[key][0] / unique_dict[key][1]
    y = (1/(1+math.exp(-5*(proportion-.5))))
    
    pos_t_dict["EDGE"].append(y)

pos_t_df = pd.DataFrame.from_dict(pos_t_dict)
with_id = with_id.reset_index(drop=True)
prop_df_reduced = pd.concat([with_id, pos_t_df], axis=1, join="inner")

in_cont_id = {"INPUT_ID" : [], "CONT_ID" : []}
for pair in prop_df_reduced["ID_PAIRS"]:
    in_id = pair.split("|")[-2]
    cont_id = pair.split("|")[-1]
    in_cont_id["INPUT_ID"].append(in_id)
    in_cont_id["CONT_ID"].append(cont_id)
in_cont_id_df = pd.DataFrame.from_dict(in_cont_id)
with_ids = pd.concat([in_cont_id_df, prop_df_reduced], axis=1)

with_ids.to_csv("Act_tanh.csv")
