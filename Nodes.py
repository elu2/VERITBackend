import pandas as pd

tanh_df = pd.read_csv("Tanh.csv")

inputs = tanh_df[["INPUT"]].rename(columns={"INPUT": "Id"})
controllers = tanh_df[["CONTROLLER"]].rename(columns={"CONTROLLER": "Id"})

nodes = inputs.append(controllers).drop_duplicates(inplace=False)

nodes.to_csv("nodes_table_all.csv", index=False)
