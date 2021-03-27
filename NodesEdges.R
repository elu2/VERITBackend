## ----setup, include=FALSE------------------------------------------------------------------------------
setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
library("tibble")
library("dplyr")

## ----Combine-------------------------------------------------------------------------------------------
# Run this chunk to combine all Activations and None Controller csv files.
# The Activations csv should be titled: all_tanh.csv
# The NONE Controllers csv should be titled: NC_all_tanh.csv
activation <- read.csv("Act_tanh.csv")
none_cont <- read.csv("NC_tanh.csv")
prop_df <- rbind(activation, none_cont)

prop_df <- prop_df %>%
  filter(!grepl(':uaz:', ID_PAIRS))
prop_df <- prop_df %>%
  filter(!grepl(':UAZ:', ID_PAIRS))

## ------------------------------------------------------------------------------------------------------
controllers=prop_df %>%
  distinct(CONTROLLER) %>%
  rename(Id=CONTROLLER)

outputs=prop_df %>%
  distinct(INPUT) %>%
  rename(Id=INPUT)

nodes <- full_join(controllers,outputs, by="Id")


## ------------------------------------------------------------------------------------------------------
# Create vector of equal weights (1)
one_vec <- rep(1, length(prop_df$TOTAL))

tibble_df <- tibble(source=prop_df$CONTROLLER, source_id=prop_df$CONT_ID, target=prop_df$INPUT, target_id=prop_df$INPUT_ID, weight=one_vec, color_col=prop_df$EDGE, thickness=prop_df$TOTAL)

## ------------------------------------------------------------------------------------------------------
# Table for edges
write.csv(tibble_df, file="edges_table.csv", row.names=FALSE)

# Table for nodes
write.csv(nodes, file="nodes_table_all.csv", row.names=FALSE)

# Thickness column add-on
write.csv(prop_df$TOTAL, file="thickness.csv", row.names=FALSE)

