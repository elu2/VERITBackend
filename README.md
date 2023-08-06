# VERIT backend

## Description

Below are the steps needed to regenerate or update the datasets used for VERIT. While reading the README, refer to the `WorkflowDiagram.pdf` chart.

## Steps:
1. Ensure all annotations ending in `*.arizona-out.tsv` are present in/across target directory(ies)

2. Run `Startup.py`
    * Reads in `pat.log.pkl` and assesses which annotations need to be rerun
    * Write out `torun.log.pkl` to tell `ActEvProc.py`, `NCEvProc.py`, and `GenProc.py` what annotations need to be run
    * Save these files to make future reruns/updates quicker

3. Run `ActEvProc.py` and `NCEvProc.py`.
    * Collects the annotations into two large files
    * Unneeded fields are not included, reducing file size
    * Order does not matter
    * `NCEvProc.py` deals with interactions that are not simply "Activation"

4. Run `GenProc.py`
    * Creates nodes, edges, and evidence files for Reach data

5. Run `Gene Post Processing.ipynb`
    * Assigns priorities to which node labels will be shown in visualization
    * Fundamental for making "Gene" queries efficient and functional
    * Extended documentation is provided within the notebook
    * Intermediate files needing to be generated from this notebook are omitted from the flowchart
    * Using UniProt's online ID mapping tool is required. Instructions provided

6. Run `BG_retrieve.sh`
    * cURLs in a prespecified BIOGRID dataset and retrieves only necessary fields
    * `BIOGRID-ALL-$VERSION.trunc.tsv` is returned

7. Run `BIOGRID Preprocess.ipynb`
    * Similar to GenProc.py in generating most of the final files for BIGORID dataset
    * Similar to `Gene Post Processing.ipynb` in requiring intermediate files that are omitted in flowchart, containing extended documentation, and needing to use UniProt's online ID mapping tool
    * Also generates a NetworkX graph (`BIOGRID_graph.pkl`) directly. Could adopt this for Reach as well, but minor thing

8. Run `write_ev.py`
    * 

9. Run `dbCombiner.py`
    * `databases` directory is included in this GitHub repo to produce the end file
    * Borrows the knowledgebases that Reach grounds to in order to provide a fully inclusive set of identifiers


## Notes:
* `*.arizona-out.tsv` directory structure may vary and may require changes in Startup.py.
* `AllAct.csv` and `AllNC.csv` should not require full reconstruction when `*.arizona-out.tsv` is updated if log files (`pat.log.pkl` and `torun.log.pkl`) are maintained.
* .ipynb notebooks include extended documentation as the procedure involves manual labor.
    * The motivation is that these are not very streamlined steps partially due to the effort required to provide an alternative. Also, it's a platform to provide better documentation.
    * Typically this includes:
        * Ensuring the correct version of pandas (1.1.5) is used to write out pickle files
        * Writing out an intermediate file of IDs, then using UniProt's (online) ID mapping tool.
* "Terminal" or final files that are read by flask_vis.py from the VERIT app are colored in light blue.
* BIOGRID version can be easily changed/updated in `BG_retrieve.sh`.


