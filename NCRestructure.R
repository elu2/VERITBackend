## ----setup------------------------------------------------------------------------------
setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
library(sqldf)
library(dplyr)

df = read.csv("base_df.csv")

unique_papers <- unique(df$SEEN_IN)

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
write.csv(none_counted_df, file="NCCount_df.csv", row.names=FALSE)
