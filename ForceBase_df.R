## ----setup------------------------------------------------------------------------------
# setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
setwd("C:/Users/ericj/REACHVisualization/")
library(sqldf)
library(dplyr)

## ----Force creation of base_df.csv------------------------------------------------------
df <- read.csv("intermediate.csv")
cleaned <- sqldf("SELECT * FROM df WHERE SEEN_IN != ''")
write.csv(cleaned, file="./base_df.csv")