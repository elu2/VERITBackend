#!/usr/bin/env python
# coding: utf-8

import pandas as pd


# This program takes a dataframe and labels the Activation(Positive) as 1 and Activation(Negative) as -1. It then cbinds it to the dataframe to create xxx_labelled.csv.

# For the basic Activation-type event labels.

# For activations:
file = "ActCount_df.csv"
df = pd.read_csv(file)

numeric_labels = {"NUM_LABEL": []}
for label in df.EVENT_LABEL:
    if label == "Activation (Negative)":
        numeric_labels["NUM_LABEL"].append(-1)
    elif label == "Activation (Positive)":
        numeric_labels["NUM_LABEL"].append(1)
    else:
        numeric_labels["NUM_LABEL"].append(0)

df = pd.concat([df, pd.DataFrame(numeric_labels)], axis=1)

df.to_csv("ActLab_df.csv")

