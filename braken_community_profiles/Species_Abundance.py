#!/usr/bin/python3

# this program takes the output braken files for each sample and find all species with abundance >= 1%
# input: output braken files
# output: species with abundance >= 1% each samples


# Upload  packages
import sys
import os
import numpy as np
import pandas as pd



class Species_Abundance:
    def __init__(self, path_of_braken_output):
        self.species_main = None
        self.path_of_braken_output = path_of_braken_output  # defines the variable into class
        self.name_by_point = None
        self.species_filter = {}
        self.species4index = None
        self.species_index = None
        self.species_main = self.create_set_species()
        self.abundance_threshold = 0

    def find_species(self):
        samples = [x for x in os.listdir(self.path_of_braken_output) if x.endswith(".tsv")] # find the files to ends with .tsv
        for sample in samples: # run loop on some file in all files
            name = sample.split("_")
            name_by_point = name[6].split(".")[0]
            samples_braken = self.path_of_braken_output + "/" + sample # append the sample name to it path
            table_s = pd.read_csv(samples_braken, sep='\t')  # Read the table containing the frequencies of species
            # table_s = table_s.drop(table_s[table_s['fraction_total_reads'] <= self.abundance_threshold].index)
            table_s = table_s.rename(columns={'fraction_total_reads': name_by_point})
            table_s = table_s.set_index('species_name').iloc[:,[6]]
            self.species_filter[name_by_point] = table_s
            # print(self.species_filter[name_by_point])


    def create_set_species(self):
        species_set = set()
        for sample in os.listdir(self.path_of_braken_output):
            with open(f'{self.path_of_braken_output}/{sample}', "r") as R:
                for line in R:
                    species_s = line.split("\t")[1]
                    species_set.add(species_s)
                self.species_main = pd.DataFrame(index=species_set)
        # return self.species_main
        # print (self.species_main)

    def marge2main(self):
        for table_s in self.species_filter.values():
            # print(table_s)
            self.species_main = pd.concat([self.species_main, table_s], axis=1, join="outer")
        print(self.species_main.shape)
        self.species_main = self.species_main.fillna(0).sort_index(0).sort_index(1)
        # print(self.species_main)
        return self.species_main.to_csv("/home/odeds/ESCO_prediction/MGX_control.csv", index=True)


def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " path_of_braken_output \n\n")

    path_of_braken_output = sys.argv[1]

    S = Species_Abundance(path_of_braken_output)
    S.find_species()
    S.marge2main()

if __name__ == '__main__':
    main()



