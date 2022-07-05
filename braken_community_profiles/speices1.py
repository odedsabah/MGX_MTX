#!/usr/bin/python3

# this program takes the output braken files for each sample and find all species with abundance >= 1%
# input: output braken files
# output: species with abundance >= 1% each samples


# Upload  packages
import sys
import os
import pandas as pd
import seaborn as sns

class species:
    def __init__(self, path_of_braken_output):
        self.path_of_braken_output = path_of_braken_output # defines the variable into class
        self.table_s = None # creat empty variable to use in find_species functions

    def find_species(self):
        samples = [x for x in os.listdir(self.path_of_braken_output) if x.endswith(".tsv")] # find the files to ends with .tsv
        for sample in samples: # run loop on some file in all files
            samples_braken = self.path_of_braken_output + "/" + sample # append the sample name to it path
            self.table_s = pd.read_csv(samples_braken, sep='\t')  # Read the table containing the frequencies of species
            species_filter = self.table_s.drop(self.table_s[self.table_s['fraction_total_reads'] <= 0.01].index) # remove all species smaller than 1%

            os.makedirs('/home/odeds/to_plot', exist_ok=True)
            species_filter.to_csv('/home/odeds/to_plot.csv')
            print(species_filter) # print the tablas after remove species

def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " path_of_braken_output \n\n")

    path_of_braken_output = sys.argv[1]

    s = species(path_of_braken_output) # alias the class to s with the path
    s.find_species() #Import of the function into class species

if __name__ == '__main__':
    main()


