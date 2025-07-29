# DEXOM in python

<a href = "https://github.com/MetExplore/dexom-python/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/maximiliansti/dexom_python"></a>
<a href="https://pypi.org/project/dexom-python/"><img alt = "PyPI Package" src = "https://img.shields.io/pypi/v/dexom-python"/></a>  
<a href="https://archive.softwareheritage.org/browse/origin/?origin_url=https://pypi.org/project/dexom-python/"><img src="https://archive.softwareheritage.org/badge/origin/https://pypi.org/project/dexom-python//"></a>
<a href="https://forgemia.inra.fr/metexplore/cbm/dexom-python/-/commits/master"><img alt="pipeline status" src="https://forgemia.inra.fr/metexplore/cbm/dexom-python/badges/master/pipeline.svg" /></a>

This is a python implementation of DEXOM (Diversity-based enumeration of optimal context-specific metabolic networks)  
The original project, which was developped in MATLAB, can be found here: https://github.com/MetExplore/dexom  
The imat implementation was partially inspired by the driven package for data-driven constraint-based analysis: https://github.com/opencobra/driven

The package can be installed using pip: `pip install dexom-python`

You can also clone the git repository with `git clone https://forge.inrae.fr/metexplore/cbm/dexom-python`  
Then install dependencies with `poetry install` (if poetry is already installed in your python environment) or `pip install -e .` 

API documentation is available here: https://dexom-python.readthedocs.io/en/stable/  
All of the commandline scripts can be called with the `-h` option to display help messages.

## Requirements
- Python 3.7 - 3.10
- CPLEX 12.10 - 22.10

### Installing CPLEX

[Free license (Trial version)](https://www.ibm.com/analytics/cplex-optimizer): this version is limited to 1000 variables and 1000 constraints, and is therefore not useable on larger models

[Academic license](https://www.ibm.com/academic/technology/data-science): for this, you must sign up using an academic email address.
 - after logging in, you can access the download for "ILOG CPLEX Optimization Studio"
 - download version 12.10 or higher of the appropriate installer for your operating system
 - install the solver 

You must then update the environment variable named PYTHONPATH (in Linux) or Path (in Windows) by adding the directory containing the `setup.py` file appropriate for your OS and python version   
Alternatively, run `python "C:\Program Files\IBM\ILOG\CPLEX_Studio1210\python\setup.py" install` and/or `pip install cplex==12.10` (with the appropriate CPLEX version number)

## Available functions

These are the different functions which are available for context-specific metabolic subnetwork extraction

### apply_gpr
The `gpr_rules.py` script can be used to transform gene expression data into reaction weights.  
It uses the gene identifiers and gene-protein-reaction rules present in the model to connect the genes and reactions.  
By default, continuous gene expression values/weights will be transformed into continuous reaction weights.  
Using the `--convert` flag will instead create semi-quantitative reaction weights with values in {-1, 0, 1}. The default proportion of these three weights is {25%, 50%, 25%}, it can be adjusted with the `--quantiles` parameter.

### iMAT
`imat_functions.py` contains a modified version of the iMAT algorithm as defined by [(Shlomi et al. 2008)](https://pubmed.ncbi.nlm.nih.gov/18711341/).  
The main inputs of this algorithm are a model file, which must be supplied in a cobrapy-compatible format (SBML, JSON or MAT), and a reaction_weight file in which each reaction is attributed a score.  
These reaction weights must be determined prior to launching imat, for example with GPR rules present in the metabolic model.  

The remaining inputs of imat are:
- `epsilon`: the activation threshold of reactions with weight > 0
- `threshold`: the activation threshold for unweighted reactions
- `full`: a bool parameter for switching between the partial & full-DEXOM implementation

In addition, the following solver parameters have been made available through the solver API:
- `timelimit`: the maximum amount of time allowed for solver optimization (in seconds)
- `feasibility`: the solver feasibility tolerance
- `mipgaptol`: the solver MIP gap tolerance

note: the feasibility determines the solver's capacity to return correct results.  
**It is absolutely necessary** to uphold the following rule: `epsilon > threshold > ub*feasibility` (where `ub` is the maximal upper bound for reaction flux in the model).

By default, imat uses the `create_new_partial_variables` function. In this version, binary flux indicator variables are created for each reaction with a non-zero weight.  
In the full-DEXOM implementation, binary flux indicator variables are created for every reaction in the model. This does not change the result of the imat function, but can be used for the enumeration methods below.

There is additionally a  `parsimonious_imat` function, which first maximizes the original iMAT objective, then minimizes the absolute sum of all reaction fluxes, thus producing a parsimonious flux distribution.

### enum_functions

Four methods for enumerating context-specific networks are available:
- `rxn_enum_functions.py` contains reaction-enumeration (function name: `rxn_enum`)
- `icut_functions.py` contains integer-cut (function name: `icut`)
- `maxdist_functions.py` contains distance-maximization (function name: `maxdist`)
- `diversity_enum_functions.py` contains diversity-enumeration  (function name: `diversity_enum`)

An explanation of these methods can be found in [(Rodriguez-Mier et al. 2021)](https://doi.org/10.1371/journal.pcbi.1008730).  
Each of these methods can be used on its own. The same model and reaction_weights inputs must be provided as for the imat function.

Additional parameters for all 4 methods are:
- `prev_sol`: an imat solution used as a starting point (if none is provided, a new one will be computed)  
- `obj_tol`: the relative tolerance on the imat objective value for the optimality of the solutions  

icut, maxdist, and diversity-enum also have two more parameters:
- `maxiter`: the maximum number of iterations to run
- `full`: set to True to use the full-DEXOM implementation  
As previously explained, the full-DEXOM implementation defines binary indicator variables for all reactions in the model. Although only the reactions with non-zero weights have an impact on the imat objective function, the distance maximization function which is used in maxdist and diversity-enum can utilize the binary indicators for all reactions. This increases the distance between the solutions and their diversity, but requires significantly more computation time.  

maxdist and div-enum also have one additional parameter:  
- `icut`: if True, an integer-cut constraint will be applied to prevent this enumeration to produce duplicate solutions

## Parallelized DEXOM for computation clusters
The folder `dexom_python/cluster_utils/` contains batch scripts which can be used for running dexom_python functions on a slurm cluster, as well as a snakemake workflow which can be used to launch enumeration functions in multiple jobs.

The script `cluster_install_dexom_python.sh` contains the necessary commands for cloning the dexom-python git repository, setting up a python virtual environement and installing all required dependencies.  
Note that this script will only work if your cluster has a python module installed at `system/Python-3.7.4` - otherwise you must use a python version which is installed on your cluster.  
Installing the CPLEX solver must be done separately. For a brief explanation on how to install the solver on Linux, refer to [this IBM Q&A page](https://www.ibm.com/support/pages/installation-ibm-ilog-cplex-optimization-studio-linux-platforms).

The snakemake workflow can be launched through the following command: (note that you must replace the `"path/to/solver"` string with the actual path to your CPLEX solver.)  
```
sbatch dexom_python/cluster_utils/submit_slurm.sh
```
If you run this command without modifying any parameters, it will execute a short DEXOM pipeline (with reaction-enumeration followed by diversity-enumeration) on a toy model.

The main parameters of the snakemake workflow can be found in the file `cluster_config.yaml`.  
Here you can define the inputs & outputs, as well as the number of parallel batches and iterations per batch.  
Note that if you want to modify the advanced parameters for DEXOM, such as the solver tolerance and threshold values, you must to so in the `dexom_python/default_parameter_values.py` file.  

This workflow uses a reaction-weights file as an input. The 

The following scripts provide some tools to visualize & analyze DEXOM results:  
- `pathway_enrichment.py` can be used to perform a pathway enrichment analysis using a one-sided hypergeometric test  
- `result_functions.py` contains the `plot_pca` function, which performs Principal Component Analysis on the enumeration solutions

*Some older scripts for running enumeration functions on a slurm cluster can be found in `dexom_python/cluster_utils/legacy`. However, it is strongly recommended to use the snakemake workflow, which is more reliable and can be adapted more easily for different applications.*


## Example scripts

### Toy models
The `toy_models.py` script contains code for generating some small metabolic models and reaction weights.  
The `toy_models/` folder contains some ready-to-use models and reaction weight files.  
The `main.py` script contains a simple example of the DEXOM workflow using one of the toy models.   
As mentioned previously, the snakemake workflow in `dexom_python/cluster_utils/` also uses a toy model as an example.

### Recon 2.2
The `example_data/` folder contains a modified version of the Recon 2.2 model [(Swainston et al. 2016)](https://doi.org/10.1007/s11306-016-1051-4) as well as some differential gene expression data which can be used to test this implementation.  
The folder already contains a reaction-weights file, which was produced with the following command:  
```
python dexom_python/gpr_rules -m example_data/recon2v2_corrected.json -g example_data/pval_0-01_geneweights.csv -o example_data/pval_0-01_reactionweights
```
Alternatively an example of how this command can be submitted to a slurm cluster is shown in `slurm_example_gpr.sh` (again, you must insert the path to your CPLEX solver in the appropriate location).

In order to use the snakemake workflow on this example dataset, you must modify some parameters in `cluster_config.yaml`:
```
model: example_data/recon2v2_corrected.json
reaction_weights: example_data/pval_0-01_reactionweights.csv
output_path: example_data_cluster_output/
```
Additionally, when using continuous reaction-weights, the solver may have difficulty finding solutions if the constraints are too strict. To relax the optimality tolerance on the objective value, modify the following parameter in the file `dexom_python/default_parameter_values.py`:
```
'obj_tol': 2e-3,
```
You can then once again start the snakemake workflow with the command:
```
sbatch dexom_python/cluster_utils/submit_slurm.sh
```

After all jobs are completed, you can analyze the results with the following commands:  
```
python dexom_python/pathway_enrichment.py -s example_data_cluster_output/all_unique_solutions.csv -m example_data/recon2v2_corrected.json -o example_data/
python dexom_python/result_functions.py -s example_data_cluster_output/all_unique_solutions.csv -o example_data/
```
The file `example_data_cluster_output/all_unique_solutions.csv` contains all unique solutions enumerated with DEXOM.  
The `.png` files in the `example_data` folder contain boxplots of the pathway enrichment tests as well as a 2D PCA plot of the binary solution vectors.

### Cell-specific reconstruction

An example of how to use DEXOM-python as a part of a cell-specific network reconstruction pipeline, including a more complete snakemake workflow, can be found here: https://forge.inrae.fr/metexplore/cbm/ocmmed

### Latest version: v2.1.1