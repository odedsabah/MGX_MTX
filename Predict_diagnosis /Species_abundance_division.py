#!/usr/bin/env python3

''' This programming accepts the tables containing the prevalence of species that have undergone a community profile
from MGX and MTX data for each sample and arranges them to run in predicted models '''

# input: Tables containing all the species in all the samples found according to the phenotype
# output: Transpose tables containing the species in columns and samples in rows without empty cells

import pandas as pd
import numpy as np
import sys

def pull_phenotype(MGX_file):
    MGX_file = MGX_file.split("/")[5].split(".")[0]
    Phenotype = MGX_file.split("_")[1]
    return Phenotype

def division_species_tables(MGX_file, MTX_file, Phenotype):

    MGX_file = pd.read_csv(MGX_file)
    MTX_file = pd.read_csv(MTX_file)
    MGX_file = MGX_file.set_index(["Unnamed: 0"])
    MTX_file = MTX_file.set_index(["Unnamed: 0"])

    division_tables = MTX_file.div(MGX_file)

    division_tables.replace([np.inf, -np.inf, np.nan, -np.nan], 0, inplace=True)
    var = division_tables[(division_tables.sum(axis=1) != 0)].T
    var["Diagnosis"] = Phenotype
    var.to_csv(f'/Users/odedsabah/Desktop/division/division_tables/{Phenotype}.csv', index=True)


def main():
    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + "MGX_file" + "MTX_file \n\n")

    MGX_file = sys.argv[1]
    MTX_file = sys.argv[2]

    division_species_tables(MGX_file, MTX_file,pull_phenotype(MGX_file))

if __name__ == '__main__':
    main()
