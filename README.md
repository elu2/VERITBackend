# REACHVisualization

Visualizing REACH-parsed papers and the links between each mention.


All papers in papers_as_tsv/ must not be empty.

Run the following command in to remove dud files in papers_as_tsv/
find . -name "*.tsv" -size -280c -delete

Refer to WorkFlowChart.pdf for description on each script and csv output.

If actually trying to replicate the workflow procedure, manually change paths in ActEvProc.py and NCEvProc.py.
