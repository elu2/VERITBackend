
df=read.csv("/Users/michellewei/Downloads/query_edges (1).csv")



#remove commas
fix_src=gsub(",","",df$source)
fix_tar=gsub(",","",df$target)
head(fix_src)
df$source <- fix_src
df$target <- fix_tar
head(df)





#Make table with nodes and labels
df_src=cbind(df$source,df$source_label)
df_tar=cbind(df$target,df$target_label)
nodes=rbind(df_src,df_tar)
nodes=nodes[!duplicated(nodes[,1]),]




#Remove source and target columns from edge list
df=subset(df, select=-c(source_label,target_label))



write.table(df,"edges_fixed.txt",fileEncoding = "UTF-8",row.names = FALSE,col.names = FALSE, quote = FALSE,sep = ",")
write.table(nodes,"nodes.txt",fileEncoding = "UTF-8",row.names = FALSE,col.names = FALSE, quote = FALSE,sep = ",")


