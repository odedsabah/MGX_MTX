import pandas as pd
import numpy as np
import sys


class merging_tables:
    def __init__(self,CD_tablas, UC_tablas, control_tablas,input_format):
        self.species_main_MGX = None
        if input_format == "Metaphlan":
            input_format = "Abundance"
        if input_format == "ESCO":
            input_format = "species_name"
        self.CD_tables = pd.read_csv(CD_tablas).set_index([input_format]).T # "Abundance" > metaphlan, "species_name" > ESCO
        self.UC_tablas = pd.read_csv(UC_tablas).set_index([input_format]).T
        self.control_tables = pd.read_csv(control_tablas).set_index([input_format]).T


    def pull_phenotype(self):
        self.CD_tables["Diagnosis"] = "CD"
        self.UC_tablas["Diagnosis"] = "UC"
        self.control_tables["Diagnosis"] = "Control"
        self.species_main_MGX = pd.concat([self.CD_tables, self.UC_tablas], axis=0, join="outer")
        self.species_main_MGX = pd.concat([self.species_main_MGX, self.control_tables], axis=0, join="outer")
        # self.species_main_MGX["Diagnosis"]  = self.species_main_MGX[["Diagnosis"]].fillna('').agg(''.join, axis=1)
        self.species_main_MGX = self.species_main_MGX.replace(["", np.NAN], 0)


        # Only to ESCO format > multiply all cells by 100 python
    def multiply_100 (self, input_format):
        if input_format == "ESCO":
            self.species_main_MGX.iloc[:, 1:-2] = -np.log(self.species_main_MGX.iloc[:, 1:-2] * 100)
            self.species_main_MGX = self.species_main_MGX.replace([np.inf, 0], np.NAN)
        else:
            pass

    def species_threshold(self):
        self.species_main = self.species_main_MGX.loc[:,self.species_main_MGX.isnull().mean() < .8] # (self.species_main_MGX == 0).mean() <= 0.8]
        self.species_main.to_csv("~/Metaphlan4_all_pheno.csv")


def main():
    if len(sys.argv) != 5:
        quit("\nUsage: " + sys.argv[0] + " <CD_tables> " + "<UC_tables> " + "<control_tables> " + "<input_format (Metaphlan OR ESCO)> \n\n")

    CD_tables = sys.argv[1]
    UC_tables = sys.argv[2]
    control_tables = sys.argv[3]
    input_format = sys.argv[4]

    M = merging_tables(CD_tablas = CD_tables, UC_tablas = UC_tables, control_tablas= control_tables, input_format = input_format)
    M.pull_phenotype()
    M.multiply_100(input_format = input_format)
    M.species_threshold()

if __name__ == '__main__':
    main()



