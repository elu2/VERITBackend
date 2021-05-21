setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
library(sqldf)

uncounted <- read.csv("AllActNC.csv")
counted_df <- sqldf("SELECT INPUT, OUTPUT, CONTROLLER, EVENT_LABEL, COUNT(*) AS COUNTER, SEEN_IN, OUTPUT_ID, CONTROLLER_ID FROM uncounted GROUP BY OUTPUT_ID, CONTROLLER_ID, EVENT_LABEL ORDER BY COUNTER DESC")

# Removes anomalous rows
cleaned <- sqldf("SELECT * FROM counted_df WHERE SEEN_IN != ''")
write.csv(cleaned, file="Counted.csv", row.names=FALSE)
