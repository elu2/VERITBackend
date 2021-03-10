## ----setup------------------------------------------------------------------------------
setwd("C:/Users/ericj/holding_folder/")
library(sqldf)
library(dplyr)


## ----Initialize rbinding base table--------------------------------------------------------------------
file_names <- list.files(path="./papers_as_tsv/")
print(length(file_names))
base <- read.table(sprintf("./papers_as_tsv/%s", file_names[1]), sep="\t", header=TRUE, fill=TRUE, quote="\"")[c(1:5, 19)]


## ----rbind all subsequent files------------------------------------------------------------------------
i = 0
for (file in file_names[2:length(file_names)]){
  
  if (i %% 100 == 0){
    print(i)
  }
  
  binder <- read.table(sprintf("./papers_as_tsv/%s", file), sep="\t", header=TRUE, fill=TRUE, quote="\"")[c(1:5, 19)]
  base <- rbind(base, binder)
  i = i + 1
}

df <- data.frame(base)

# Rename columns without period incompatibilities
colnames(df) <- c("INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "SEEN_IN")

# Remove anomalous rows
df <- sqldf("SELECT * FROM df WHERE SEEN_IN != ''")


## ----Find Unique Inputs--------------------------------------------------------------------------------
# Number of unique pairs
sqldf("SELECT COUNT(*) from (SELECT distinct INPUT,CONTROLLER FROM df)")


## ----Only Pos Neg Activations--------------------------------------------------------------------------
# Here, all "NONE" Controllers are omitted. So, transcription, sumoylation, etc. are not in this dataframe.
pos_neg_counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN FROM df WHERE CONTROLLER!='NONE' GROUP BY OUTPUT, CONTROLLER, EVENT_LABEL ORDER BY COUNTER DESC")


## ------------------------------------------------------------------------------------------
# All Pos/Neg Activation event pairs
write.csv(pos_neg_counted_df, file = "./ActCount_df.csv", row.names=FALSE)


## ----Unlabelled dataframe for NONE Controllers---------------------------------------------------------
all_df <- data.frame()

for (paper in unique_papers){
  # Subset of individual paper
  pap_sub <- sqldf(sprintf("SELECT * FROM df WHERE SEEN_IN ='%s'", paper))
  
  # Subset of subset of paper: wherever controller is NONE
  eId_sub <- sqldf("SELECT INPUT, EVENT_ID, EVENT_LABEL FROM pap_sub WHERE CONTROLLER = 'NONE'")
  
  # Inputs as events are joined together
  in_id_shared <- inner_join(pap_sub, eId_sub, by=c("INPUT" = "EVENT_ID"))
  in_id_shared$EVENT_LABEL.x <- paste(in_id_shared$EVENT_LABEL.x, in_id_shared$EVENT_LABEL.y)
  relevant <- in_id_shared[c(1, 2, 3, 4, 5, 6)]
  colnames(relevant)[5] <- "EVENT_LABEL"
  
  all_df <- rbind(all_df, relevant)
}

none_counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN FROM all_df GROUP BY OUTPUT, CONTROLLER, EVENT_LABEL ORDER BY COUNTER DESC")


## ------------------------------------------------------------------------------------------------------
write.csv(none_counted_df, file="./NCCount_df.csv", row.names=FALSE)


