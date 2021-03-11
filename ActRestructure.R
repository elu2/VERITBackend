## ----setup------------------------------------------------------------------------------
setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
library(sqldf)
library(dplyr)

df = read_csv("base_df.csv")

## ----Only Pos Neg Activations--------------------------------------------------------------------------
# Here, all "NONE" Controllers are omitted. So, transcription, sumoylation, etc. are not in this dataframe.
pos_neg_counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN FROM df WHERE CONTROLLER!='NONE' GROUP BY OUTPUT, CONTROLLER, EVENT_LABEL ORDER BY COUNTER DESC")


## ------------------------------------------------------------------------------------------
# All Pos/Neg Activation event pairs
write.csv(pos_neg_counted_df, file = "./ActCount_df.csv", row.names=FALSE)
