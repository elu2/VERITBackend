import pandas as pd


def into_two(string):
    split_string = string.split(":")
    split_id = split_string[-2] + ":" + split_string[-1]
    split_name = string.split(":")[0]
    
    if "." in split_id:
        split_id = split_id.split(".")[0]
    
    return split_name, split_id


nodes_table = pd.read_csv("nodes_table_all.csv", encoding="UTF-8")
nodes_table_dict = nodes_table.to_dict()
nodes_table_dict["Label"] = []
nodes_table_dict["Only_Id"] = []

i = 0
for i in range(len(nodes_table_dict["Id"])):
    try:
        name, only_id = into_two(nodes_table_dict["Id"][i])
        nodes_table_dict["Label"].append(name)
        nodes_table_dict["Only_Id"].append(only_id)
    except IndexError:
        name = nodes_table_dict["Id"][i]
        only_id = "NotFound"
        nodes_table_dict["Label"].append(name)
        nodes_table_dict["Only_Id"].append(only_id)
    i += 1

nodes_table_dict["Label"] = pd.Series(nodes_table_dict["Label"])
nodes_table_dict["Only_Id"] = pd.Series(nodes_table_dict["Only_Id"])

nodes_table_all_labelled = pd.DataFrame(nodes_table_dict)
nodes_table_all_labelled.to_csv("nodes_table_all_labelled.csv", index=False)
