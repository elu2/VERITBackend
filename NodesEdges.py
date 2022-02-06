import pandas as pd

tanh_df = pd.read_csv("Tanh.csv", encoding='utf-8')

inputs = tanh_df[["INPUT"]].rename(columns={"INPUT": "Id"})
controllers = tanh_df[["CONTROLLER"]].rename(columns={"CONTROLLER": "Id"})

nodes = inputs.append(controllers).drop_duplicates(inplace=False)

nodes.to_csv("nodes_table_all.csv", index=False)

# -------------------------------------------------------------------------------

rename_dict = {
    "CONTROLLER": "source",
    "CONT_ID": "source_id",
    "INPUT": "target",
    "INPUT_ID": "target_id",
    "EDGE": "color_col",
    "TOTAL": "thickness"
              }

tanh_df = tanh_df.rename(columns = rename_dict)
tanh_df = tanh_df[["source","source_id","target","target_id","color_col","thickness"]]
tanh_df = tanh_df[tanh_df.source.str.contains("::")]
tanh_df = tanh_df[tanh_df.target.str.contains("::")]
tanh_df.to_csv("edges_table.csv", index=False)
