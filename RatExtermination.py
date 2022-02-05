# This script manually deletes common REACH misreads. In this instance, "mice" was a species that REACH kept reading
# as important. Thousands of times...

import pandas as pd


# rat_df: dataframe to prune from
# pest_str: string to filter out
def exterminator(rat_df, pest_strs):
    rat_df = rat_df[rat_df.CONTROLLER.str.contains("::")]
    rat_df = rat_df[rat_df.OUTPUT.str.contains("::")]
    
    for tstr in pest_strs:
        rat_df = rat_df[~rat_df.CONTROLLER.str.contains(tstr)]
        rat_df = rat_df[~rat_df.OUTPUT.str.contains(tstr)]
    return rat_df


df1 = pd.read_csv("Counted.csv", encoding="utf-8").astype(str)
df2 = pd.read_csv("AllActNC.csv", encoding="utf-8").astype(str)

pest_strs = [":uaz:", "mice:"]

df1_ext = exterminator(df1, pest_strs)
df2_ext = exterminator(df2, pest_strs)

df1_ext.to_csv("Counted.csv")
df2_ext.to_csv("AllActNC.csv")
