#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# For NONE CONTROLLERS:
# Gets rid of the .x suffixes. All the information needed is already provided by EVENT_LABEL column.
df = pd.read_csv("NCCount_df.csv", encoding="UTF-8")

redone_dict = {
    "OUTPUT" : [],
    "CONTROLLER" : []
}

outputs = df["OUTPUT"]
controllers = df["CONTROLLER"]

for i in range(len(outputs)):
    if "." in outputs[i]:
        redone_dict["OUTPUT"].append(outputs[i][:outputs[i].index(".")])
    else:
        redone_dict["OUTPUT"].append(outputs[i])

for i in range(len(controllers)):
    if "." in controllers[i]:
        redone_dict["CONTROLLER"].append(controllers[i][:controllers[i].index(".")])
    else:
        redone_dict["CONTROLLER"].append(controllers[i])

df2 = pd.DataFrame.from_dict(redone_dict)

df["OUTPUT"] = df2["OUTPUT"]
df["CONTROLLER"] = df2["CONTROLLER"]

# Label each pairing with a numeric value.
numeric_labels = {"NUM_LABEL": []}
for label in df.EVENT_LABEL:
    # If anomalous label is hit, ignore.
    try:
        _, pos_neg, label_type = label.split(" ")
    except ValueError:
        continue
    
    if pos_neg == "(Negative)": 
        if label_type == "Amount":
            numeric_labels["NUM_LABEL"].append(1)
        elif label_type == "Transcription":
            numeric_labels["NUM_LABEL"].append(-1)
        elif label_type == "Ubiquitination":
            numeric_labels["NUM_LABEL"].append(1)
        else:
            numeric_labels["NUM_LABEL"].append(0)

    elif pos_neg == "(Positive)":
        if label_type == "Amount":
            numeric_labels["NUM_LABEL"].append(-1)
        elif label_type == "Transcription":
            numeric_labels["NUM_LABEL"].append(1)
        elif label_type == "Ubiquitination":
            numeric_labels["NUM_LABEL"].append(-1)
        else:
            numeric_labels["NUM_LABEL"].append(0)


df = pd.concat([df, pd.DataFrame(numeric_labels)], axis=1)

df.to_csv("NCLab_df.csv")
