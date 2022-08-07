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
    MGX_file = MGX_file.loc[:,MTX_file.columns] # keep over only examples found in both MGX and MTX
    MGX_file = MGX_file.T.replace(0, np.nan)
    MTX_file = MTX_file.T.replace(0, np.nan)

    division_tables = MTX_file.iloc[:,1:].div(MGX_file.iloc[:,1:])
    division_tables.replace([np.nan, -np.nan], 0, inplace=True)
    division_tables = division_tables.loc[:,(division_tables**2).sum() != 0]

    division_tables = pd.concat([division_tables,MGX_file["Diagnosis"]], axis =1 )
    division_tables.to_csv(f'/Users/odedsabah/Desktop/division_tables.csv', index=True)



def main():
    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + "MGX_file" + "MTX_file \n\n")

    MGX_file = sys.argv[1]
    MTX_file = sys.argv[2]

    division_species_tables(MGX_file, MTX_file)

if __name__ == '__main__':
    main()
