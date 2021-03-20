#!/usr/bin/env python
# coding: utf-8

import pandas as pd


# For NONE CONTROLLERS:
file = "NCCount_df.csv"
df = pd.read_csv(file)

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
