# **Nagilums Tree**

Monogenic diabetes is a rare form of paediatric diabetes caused by a variation in a single gene responsible for pancreatic β-cell insulin production. Dysfunction of 
these genes results in insulin suppression which in turn causes hyperglycaemic health conditions. Maturity-onset diabetes of the young (MODY) is a sub-type of monogenic 
diabetes, presenting in age groups below 35. Roughly 2 – 5 % of diabetic cases are diagnosed as MODY, however, patient classification has revealed symptomatic cohorts that are undiagnosed. 
It is speculated that these cases are a result of unknown genetic variants. It is necessary to identify pathogenic variants responsible for MODY to avoid common misdiagnosis and provide specialized medical care.

Through the integration of genomics and proteomics, the field of proteogenomics allows for the identification of alternative forms of proteins resulting from genomic variation. Then, spectra acquired by mass-spectrometry are matched to a sequence database, yielding peptide spectrum matches of different levels of confidence. However, discriminating between variant and canonical peptides remains challenging due to similarities between the sequences.
To this end, a classifier system is designed in this work to process a PSM dataset using the target-decoy approach.

The script files provided here are written in Python using PyCharm v3.10. 
The classifier enacts a machine learning base learner created using the Scikit-learn library (https://scikit-learn.org/stable/) 

Three implementation tasks are incorporated into this pipeline using the same classifier system and different statistical inferences and graphical visualisation methods. Details of this method are explained in the MSc thesis entitled: ""

A brief description of the tasks are provided below:

## [**Task 1: Comparison of ML architectures**](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/5c9c79f221e35b1ff1c3559e8c39d1f4b26dc041/Task%201%3A%20Comparison%20of%20ML%20architectures)
The folder [decision tree ensemble models](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/d644e651a57059bc12393dcc9ff87d53cbad9030/Task%201%3A%20Comparison%20of%20ML%20architectures/Decision%20tree%20ensemble%20models) contains five Python files, one for each of the decision tree ensmeble architectures:
- Random Forest
- ExtraTree
- Gradient Boosting
- Histogram-based Gradient Boosting
- XGBoost

The [Calculations](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/d644e651a57059bc12393dcc9ff87d53cbad9030/Task%201%3A%20Comparison%20of%20ML%20architectures/Calculations.py) file is required to be in place for the classification system to execute calculations concerning the FDR and confusion matrix

The output is a .csv file saved locally onto a personal system.
The [Graphical visualisation](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/d644e651a57059bc12393dcc9ff87d53cbad9030/Task%201%3A%20Comparison%20of%20ML%20architectures/graphical_visualisation.py) file is setup to receive all 5 files and return figures of:
- AUROC curve
- PR curve
- Histograms
- Cumulative count comparisons
- FDR distribution comparison

The figures will receive the appropriate title of the architecture with all legends and descriptors.

## [Task 2: Decoy variant concept](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/d28b746a761f2ab74cacc4da54df617b8f6cae44/Task%202%3A%20Decoy%20variant%20concept)
This folder contains the Python files required to conduct the [decoy variant strategy](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/d644e651a57059bc12393dcc9ff87d53cbad9030/Task%202%3A%20Decoy%20variant%20concept/decoy_variant_search_strategy.py) and the [decoy seq strategy](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/d644e651a57059bc12393dcc9ff87d53cbad9030/Task%202%3A%20Decoy%20variant%20concept/decoy_sequence_search_strategy.py). 

The [Calculations](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/7c0a953b74b20ededd308a6e809693ac82909dfc/Task%202%3A%20Decoy%20variant%20concept/calculations.py) Python file is required to be in place for the classification system to execute calculations concerning FDR, PEP and confusion matrix.

The files are setup to iterate through a local folder containing the iPSC PSM data files. Classification is setup for the ExtraTrees architecture under the Scikit-learn library. The classified PSM datasets are saved locally as .csv files with the appropriate names of the iPSC development stage (Stage 0 and Stage 4) and cell type (wild type and mutant).

The [Graphical visualisation](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/7c0a953b74b20ededd308a6e809693ac82909dfc/Task%202%3A%20Decoy%20variant%20concept/graphical_visualisation.py) file is setup to receive all 12 for both the _decoy variant strategy_ and _decoy seq strategy_ files and return figures from [plots_and_figures](https://github.com/lorensha/Nagilums-Tree-pipeline/blob/7c0a953b74b20ededd308a6e809693ac82909dfc/Task%202%3A%20Decoy%20variant%20concept/plots_and_figures.py):
- Histograms
- Cumulative count of PEP comparisons
- PEP distribution plots

## [Task 3: MODY expression analysis](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/d28b746a761f2ab74cacc4da54df617b8f6cae44/Task%203%3A%20MODY%20expression%20analysis)

The [MODY gene .txt. files](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/34b3c6ae746f9e9fafa00be669a3bb4acac98391/Task%203%3A%20MODY%20expression%20analysis/MODY%20gene%20.txt%20files) folder contains a file of the 14 MODY genes and a collective list of possible MODY genes

The [MODY expression plots](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/9fee31449552b9f23c6e5a45c34d594094576869/Task%203%3A%20MODY%20expression%20analysis/MODY%20expression%20plots) folder contains the Python files to create the MODY PEP expression plots visualised in the Thesis, supplementary figures of the collective MODY list and MODY expression of the variant PSMs only.

The protein-protein interaction network map is created using STRING API for future works and the Python file is included in this folder.
