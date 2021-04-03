#!/usr/bin/env python
# coding: utf-8

import pandas as pd


# This program takes a dataframe and labels the Activation(Positive) as 1 and Activation(Negative) as -1. It then cbinds it to the dataframe to create xxx_labelled.csv.

# For the basic Activation-type event labels.

# For activations:
# Gets rid of the .x suffixes. All the information needed is already provided by EVENT_LABEL column.
df = pd.read_csv("ActCount_df.csv", encoding="UTF-8")

redone_dict = {
    "OUTPUT" : [],
    "CONTROLLER" : []
}

outputs = df["OUTPUT"]
controllers = df["CONTROLLER"]

for i in range(len(outputs)):
    if "." in str(outputs[i]):
        redone_dict["OUTPUT"].append(outputs[i][:outputs[i].index(".")])
    else:
        redone_dict["OUTPUT"].append(outputs[i])

for i in range(len(controllers)):
    if "." in str(controllers[i]):
        redone_dict["CONTROLLER"].append(controllers[i][:controllers[i].index(".")])
    else:
        redone_dict["CONTROLLER"].append(controllers[i])

df2 = pd.DataFrame.from_dict(redone_dict)

df["OUTPUT"] = df2["OUTPUT"]
df["CONTROLLER"] = df2["CONTROLLER"]

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
