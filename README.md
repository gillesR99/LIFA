# LFIA color analysis

Python script to analyse C-reactive protein (CRP) concentration via color intensity.

## Directory Structure

```bash
- lfia_lab
  ├ data/                  # data files from the microscope
  ├ REAMDME.md             # this file
  ├ lfia_lab_env.yml       # file to create conda environment
  ├ lfia_data_analysis.py  # python script to analyse datafiles
  ├ tif_parser.py          # parser to read in the tif files
  ├ comparison_plot.py     # comparison plot  (green channel intensity over concentration
```

## Setup Conda Environment

```bash
# create conda environment
conda env create -f lfia_lab_env.yml
# activate environemnt
conda activate lfia_lab
```

## Handy Commands

```bash
# activate environemnt
conda activate lfia_lab

# deactivate environemnt
conda deactivate

# install package $PACKAGE_NAME via conda
conda install $PACKAGE_NAME

# export environment to yaml file
conda env export | grep -v "^prefix: " > lfia_lab_env.yml
```
