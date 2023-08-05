import pandas as pd
import pickle


def pickler(to_pickle):
    to_pickle_csv = pd.read_csv(to_pickle, encoding="utf-8")#, sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1)
    pickle.dump(to_pickle_csv, open(f"{to_pickle.split('.')[0]}.pkl", "wb"))
    print(f"Pickled {to_pickle.split('.')[0]}")

pickler("nodes_table_all_labelled.csv")