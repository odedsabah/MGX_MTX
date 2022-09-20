#!/usr/bin/env python3

''' This programming accepts the tables containing the prevalence of species that have undergone a community profile
from MGX and MTX data for each sample and arranges them to run in predicted models '''

# input: Tables containing all the species in all the samples found according to the phenotype
# output: Transpose tables containing the species in columns and samples in rows without empty cells

import pandas as pd
import numpy as np
import sys


# def pull_phenotype(MGX_file):
#     MGX_file = MGX_file.split("/")[5].split(".")[0]
#     Phenotype = MGX_file.split("_")[1]
#     return Phenotype

def division_species_tables(MGX_file, MTX_file):

    MGX_file = pd.read_csv(MGX_file).T
    MTX_file = pd.read_csv(MTX_file).T
    MGX_file = MGX_file.rename(columns=MGX_file.iloc[0]).drop(MGX_file.index[0])
    MTX_file = MTX_file.rename(columns=MTX_file.iloc[0]).drop(MTX_file.index[0])
    MGX_file = MGX_file.loc[:,MTX_file.columns].T # keep over only examples found in both MGX and MTX
    MTX_file = MTX_file.T
    MGX_file.insert((len(MGX_file.columns)-1), "Diagnosis", MGX_file.pop("Diagnosis"))
    MTX_file.insert((len(MTX_file.columns)-1), "Diagnosis", MTX_file.pop("Diagnosis"))

    MGX_file_ = MGX_file.loc[:, MGX_file.columns != "Diagnosis"]
    MTX_file_ = MTX_file.loc[:, MTX_file.columns != "Diagnosis"]

    MGX_file_ = MGX_file_.replace(0, np.nan)
    MTX_file_ = MTX_file_.replace(0, np.nan)
    # print(MGX_file_)
    # print(MTX_file_)

    division_tables = MTX_file_.div(MGX_file_)

    division_tables = division_tables.loc[:,division_tables.columns.str.startswith('s__')]

    # division_tables = division_tables.loc[:,(division_tables**2).sum() != 0]
    division_tables = pd.concat([division_tables, MTX_file["Diagnosis"]], axis =1)
    division_tables = division_tables.loc[:,division_tables.isnull().mean() < .8]
    division_tables.replace([np.nan, -np.nan] ,0 , inplace=True)
    division_tables.to_csv('~/MGX_VS_MTX_mp4.csv', index=True)


def main():
    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + "MGX_file" + "MTX_file \n\n")

    MGX_file = sys.argv[1]
    MTX_file = sys.argv[2]

    division_species_tables(MGX_file, MTX_file)

if __name__ == '__main__':
    main()
