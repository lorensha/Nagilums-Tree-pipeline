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

## [**Task 1: Comparison of ML architectures**]([https://github.com/lorensha/Nagilums_Tree/tree/991e08fc209da806fcd8240d57f25fe3b28ce680/Task%20One%3A%20comparison%20of%20architectures](https://github.com/lorensha/Nagilums-Tree-pipeline/tree/5c9c79f221e35b1ff1c3559e8c39d1f4b26dc041/Task%201%3A%20Comparison%20of%20ML%20architectures)
The folder [decision tree ensemble models](https://github.com/lorensha/Nagilums_Tree/tree/0ae9faa007e849417073d18e1956149bad91e735/Task%20One%3A%20comparison%20of%20architectures/decision%20tree%20ensemble%20models) contains five Python files, one for each of the decision tree ensmeble architectures:
- Random Forest
- ExtraTree
- Gradient Boosting
- Histogram-based Gradient Boosting
- XGBoost

The [Calculations]() file is required to be in place for the classification system to execute calculations concerning the FDR and confusion matrix

The output is a .csv file saved locally onto a personal system.
The [Graphical visualisation]() file is setup to receive all 5 files and return figures of:
- AUROC curve
- PR curve
- Histograms
- Cumulative count comparisons
- FDR distribution comparison

The figures will receive the appropriate title of the architecture with all legends and descriptors.

## [Task 2: Decoy variant concept]()

