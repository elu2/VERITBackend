# REACHVisualization
Visualizing REACH-parsed papers and the links between each mention.

When creating the concatenated, full dataframe of all az-out.tsv files, change path to your local directory with the az-out.tsv files after cloning. Make sure that each file in this directory is not empty. The name should be "papers_as_tsv".

The nodes table output as of now has two columns: "label" and "Label". When importing into gephi/cytoscape, it's necessary to manually change "label" to "Id".

Run the following command in to remove dud files in papers_as_tsv/
find . -name "*.tsv" -size -280c -delete
