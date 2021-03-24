#Create edge and node lists that have the correct format for visualization
#Outputs query_nodes_fixed.txt and query_edges_fixed.txt
Rscript clean_query_tables.R

#Create visualization (outputs file called reach.subset.dot.png)
python make_visualization.py
