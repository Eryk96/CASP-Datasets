# CASP-Datasets
ETL pipelines for producing Critical Assessment of Protein Structure Prediction (CASP) datasets for AI models and analysis

## Getting started

You can either download the datasets or run the project. The current datasets does only include PDB entries that are from the FM (free modelling) category. If you want to build datasets that include additional categories you can edit the ```class_filter``` from the config files.

**Requirements**
- Python 3.8+

**Installation**

Clone the directory and create a virtual environment inside the repository.

```git clone <repository>```\
```python -m venv venv```

Activate the virtual environment

```source venv/bin/activate```

Install dependencies and the casp

```python setup.py install```\
```pip install -r requirements.txt```

Run the pipeline

```casp run -c config/casp14.yml```

## CASP Datasets

The datasets are found in the data folder. They are organized by the competition number. In each of the folders there is a dataset of the **FM domain** CASP protein that have been merged into a single dataset. Additionally you can find DSSP files entries, domain summary and fasta files of the entries.

[CASP14]() \\
[CASP13]() \\
[CASP12]() \\
[CASP11]() \\
