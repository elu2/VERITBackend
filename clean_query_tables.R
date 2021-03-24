#setwd("/xdisk/guangyao/REACH2/REACHVisualization/")
nodes_df=read.csv("query_nodes.csv",header = TRUE)
edges_df=read.csv("query_edges.csv",header = TRUE)
edges_df=subset(edges_df, select=-c(source_lab,target_lab))
nodes_df=subset(nodes_df, select=-c(FullName)) 


#remove commas
fix_nodes_id=gsub(",","",nodes_df$Id)
fix_nodes_lab=gsub(",","",nodes_df$Label)
fix_edges_src=gsub(",","",edges_df$source)
fix_edges_tar=gsub(",","",edges_df$target)
nodes_df$Id <- fix_nodes_id
nodes_df$Label <- fix_nodes_lab
edges_df$source <- fix_edges_src
edges_df$target <- fix_edges_tar

#replace weight column with thickness column
edges_df$weight <- edges_df$thickness

#Take square root of thickness column so the edges aren't too big for the large values
edges_df$thickness <- trunc(sqrt(edges_df$thickness))

write.table(edges_df,"query_edges_fixed.txt",fileEncoding = "UTF-8",row.names = FALSE,col.names = FALSE, quote = FALSE,sep = ",")
write.table(nodes_df,"query_nodes_fixed.txt",fileEncoding = "UTF-8",row.names = FALSE,col.names = FALSE, quote = FALSE,sep = ",")