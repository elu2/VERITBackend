## ----setup------------------------------------------------------------------------------
# setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
# setwd("C:/Users/ericj/REACHVisualization/")
setwd("C:/Users/ericj/testing_site/")

library(sqldf)
library(dplyr)


## ----Initialize rbinding base table--------------------------------------------------------------------
file_names <- list.files(path="./papers_as_tsv/")
print(length(file_names))


## ----rbind all subsequent files------------------------------------------------------------------------
# To start from beginning: use 1 as lower bound for index. To start from wherever left off, change lower bound to what log last reads.
base <- data.frame(matrix(ncol = 6, nrow = 0))
names <- c("INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "SEEN_IN")
colnames(base) <- names
write.table(base, file="intermediate.csv", row.names=FALSE, sep=",", append=TRUE, col.names=TRUE)

i = 0
for (file in file_names[1:length(file_names)]){
  
  if (i %% 100 == 0){
    # Rename columns before appending
    names <- c("INPUT", "OUTPUT", "CONTROLLER", "EVENT_ID", "EVENT_LABEL", "SEEN_IN")
    colnames(base) <- names
    write.table(base, file="intermediate.csv", row.names=FALSE, sep=",", append=TRUE, col.names=FALSE)
    
    # Keep track of writes with log
    write.table(paste(Sys.time(), ": ", i, " papers in dataframe."), file = "Combinetsvs.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)

    # Reinitialize empty base and dump past info
    base <- data.frame(matrix(ncol = 6, nrow = 0))

  }
  
  binder <- read.table(sprintf("./papers_as_tsv/%s", file), sep="\t", header=TRUE, fill=TRUE, quote="\"")[c(1:5, 19)]
  base <- rbind(base, binder)
  i = i + 1
}

# To get the last <100 papers.
write.table(base, file="intermediate.csv", row.names=FALSE, sep=",", append=TRUE)
write.table(paste(Sys.time(), ": ", i, " papers in dataframe."), file = "Combinetsvs.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)
# Appends finished
write.table("***RAN TO COMPLETION***", file = "Combinetsvs.log", row.name=FALSE, col.names=FALSE, append=TRUE, quote=FALSE)

# Then remove anomalous files.
df <- read.csv("intermediate.csv")
cleaned <- sqldf("SELECT * FROM df WHERE SEEN_IN != ''")
write.csv(cleaned, file="base_df.csv", row.names=FALSE)
