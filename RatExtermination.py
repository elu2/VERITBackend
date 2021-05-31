# This script manually deletes common REACH misreads. In this instance, "mice" was a species that REACH kept reading
# as important. Thousands of times...

import pandas as pd


# rat_df: dataframe to prune from
# pest_str: string to filter out
def exterminator(rat_df, pest_str):
    rat_df = rat_df[~rat_df.CONTROLLER.str.contains(pest_str)]
    exterminated = rat_df[~rat_df.OUTPUT.str.contains(pest_str)]
    return exterminated


df1 = pd.read_csv("Counted.csv", encoding="utf-8")
df2 = pd.read_csv("AllActNC.csv", encoding="utf-8")

df1_ext = exterminator(df1, "mice:")
df2_ext = exterminator(df2, "mice:")

df1_ext.to_csv("Counted.csv")
df2_ext.to_csv("AllActNC.csv")
