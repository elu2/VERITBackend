## ----setup------------------------------------------------------------------------------
# setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
setwd("C:/Users/ericj/REACHVisualization/")
library(sqldf)
library(dplyr)

## ----Force creation of NCCounted_df.csv------------------------------------------------------
uncounted <- read.csv("NCCount_df_inter.csv")
none_counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN FROM uncounted GROUP BY OUTPUT, CONTROLLER, EVENT_LABEL ORDER BY COUNTER DESC")

write.csv(none_counted_df, file="NCCount_df.csv", row.names=FALSE)
