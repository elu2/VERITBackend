import pandas as pd
import pickle

# Read in pubchem db file with new col names
pubchem_df = pd.read_csv("./knowledgebases/pubchemdb.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1)
chebi_df = pd.read_csv("./knowledgebases/chebidb.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1)
proteins0f_df = pd.read_csv("./knowledgebases/proteins0f.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1).drop(2, axis=1).drop_duplicates().reset_index(drop=True)
proteinsgp_df = pd.read_csv("./knowledgebases/proteinsgp.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1).drop(2, axis=1).drop_duplicates().reset_index(drop=True)
proteinsqz_df = pd.read_csv("./knowledgebases/proteinsqz.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1).drop(2, axis=1).drop_duplicates().reset_index(drop=True)
mesh_df = pd.read_csv("./knowledgebases/meshdb.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1)
gobioproc_df = pd.read_csv("./knowledgebases/gobioproc.tsv", encoding="utf-8", sep="\t", header=None).rename({0:"name", 1:"id"}, axis=1).drop([2, 3], axis=1).drop_duplicates().reset_index(drop=True)


# Adds pubchem tag to ids
# For some reason CHEBI and GO is already tagged
def tagger(spec_id, db_name):
    return str(db_name + str(spec_id))


pubchem_df["id"] = pubchem_df.id.apply(tagger, db_name="pubchem:")
proteins0f_df["id"] = proteins0f_df.id.apply(tagger,db_name="uniprot:")
proteinsgp_df["id"] = proteinsgp_df.id.apply(tagger,db_name="uniprot:")
proteinsqz_df["id"] = proteinsqz_df.id.apply(tagger,db_name="uniprot:")
mesh_df["id"] = mesh_df.id.apply(tagger, db_name="mesh:")


full_df = pubchem_df
full_df = full_df.append(mesh_df)
full_df = full_df.append(chebi_df)
full_df = full_df.append(gobioproc_df)
full_df = full_df.append(proteins0f_df)
full_df = full_df.append(proteinsgp_df)
full_df = full_df.append(proteinsqz_df).reset_index(drop=True)

# Turns all names into lower case
full_df["name"] = full_df.name.apply(lambda a: str(a).lower())

pickle.dump(full_df, open("./knowledgebases/combinedDBs.pkl", "wb"))
