import pandas as pd

def check(queries_id):
    edges_table = pd.read_csv("edges_table.csv", encoding="latin-1")
    sources = edges_table["source_id"].tolist()
    targets = edges_table["target_id"].tolist()
    color_col = edges_table["color_col"].tolist()

    all_species = list(set(sources + targets))
    not_in=[]

    for query in queries_id:
        if query not in all_species:
            not_in.append(f"{query}\n")
        else:
            continue
            
    return not_in

   
