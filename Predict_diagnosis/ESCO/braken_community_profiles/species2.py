#!/usr/bin/env python3

import os
import pandas as pd
import sys

BRACKEN_SPECIES_COLUMNS_INDEX = 1
BRACKEN_ABUNDANCE_SPECIES_COLUMNS_INDEX = 7

def create_dict_index(tabla_species):
    dict_index = {}
    f = open(tabla_species,"r")
    f.readline()
    for line in f:
        line_part = line.split()
        dict_index[line_part[BRACKEN_SPECIES_COLUMNS_INDEX]] = float(line_part[BRACKEN_ABUNDANCE_SPECIES_COLUMNS_INDEX])
    f.close()
    return dict_index

def create_set_species(path):
    species_set = set()
    for sample in os.listdir(path):
        print(sample)
        species_set.update(create_dict_index(os.path.join(path, sample)).keys())
        print(species_set)
    return species_set

def create_abundance_vector(species_vector,path_bracken):
    abundance_vector = []
    species_abundance = create_dict_index(path_bracken)
    for species in species_vector:
        abundance_vector.append(species_abundance.get(species,0))
    return abundance_vector

def main_table(path):
    global name_by_point
    species_vector = list(create_set_species(path))
    species_vector.sort()
    df_species = pd.DataFrame()
    df_species["species"] = species_vector
    for sample in os.listdir(path):
        name = sample.split("_")
        name_by_point = name[6].split(".")[0]
        df_species[name_by_point] = create_abundance_vector(species_vector,os.path.join(path, sample))
    return df_species.drop(df_species[df_species[name_by_point] <= 0.01 ].index)

def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " path_of_braken_output \n\n")

    path_of_braken_output = sys.argv[1]
    df = main_table(path_of_braken_output)
    df.to_csv("/home/odeds/out_species.tsv", index= False, sep= "\t")
    df.to_csv("/home/odeds/out_species.csv", index= False)

if __name__ == '__main__':
    main()
