## ----setup------------------------------------------------------------------------------
setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
library(sqldf)
library(dplyr)

file_names <- list.files(path="./papers_as_tsv/")
names <- c("INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "SEEN_IN")
column_classes <- c("character", "character", "character", "character", "character", "character")
NC_intermediate <- data.frame(matrix(ncol = 6, nrow = 0))
colnames(NC_intermediate) <- names
write.table(NC_intermediate, file="NCCount_df_inter.csv", row.names=FALSE, col.names=TRUE, sep=",", append=TRUE)

## ----Unlabelled dataframe for NONE Controllers---------------------------------------------------------
NC_intermediate <- data.frame(matrix(ncol = 6, nrow = 0))

i = 0
for (file in file_names[1:length(file_names)]){
  if (i %% 100 == 0){
    write.table(NC_intermediate, file="NCCount_df_inter.csv", row.names=FALSE, col.names=FALSE, sep=",", append=TRUE)
    NC_intermediate <- data.frame(matrix(ncol = 6, nrow = 0))
    # Keep track of writes with log
    write.table(paste(Sys.time(), ": ", i, " NC papers counted."), file = "NCCounting.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)
  }
  
  pap_sub <- read.table(sprintf("./papers_as_tsv/%s", file), sep="\t", header=TRUE, fill=TRUE, quote="\"", colClasses=column_classes)[c(1:5, 19)]
  colnames(pap_sub) <- names

  # Subset of paper: wherever controller is NONE
  eId_sub <- sqldf("SELECT INPUT, EVENT_ID, EVENT_LABEL FROM pap_sub WHERE CONTROLLER = 'NONE'")
  
  # Inputs as events are joined together
  in_id_shared <- inner_join(pap_sub, eId_sub, by=c("INPUT" = "EVENT_ID"))
  in_id_shared$EVENT_LABEL.x <- paste(in_id_shared$EVENT_LABEL.x, in_id_shared$EVENT_LABEL.y)
  relevant <- in_id_shared[c(1, 2, 3, 4, 5, 6)]
  colnames(relevant)[5] <- "EVENT_LABEL"
  
  NC_intermediate <- rbind(NC_intermediate, relevant)
  i = i + 1
}

# To get the last <100 papers.
write.table(NC_intermediate, file="NCCount_df_inter.csv", row.names=FALSE, col.names=FALSE, sep=",", append=TRUE)
write.table(paste(Sys.time(), ": ", i, " papers in dataframe."), file = "NCCounting.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)
# All appends have been finished.
write.table("***RAN TO COMPLETION***", file = "NCCounting.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)

uncounted <- read.csv("NCCount_df_inter.csv")
none_counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN FROM uncounted GROUP BY OUTPUT, CONTROLLER, EVENT_LABEL ORDER BY COUNTER DESC")

write.csv(none_counted_df, file="NCCount_df.csv", row.names=FALSE)
