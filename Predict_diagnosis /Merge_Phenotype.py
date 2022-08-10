import pandas as pd
import numpy as np
import sys


class merging_tables:
    def __init__(self,CD_tablas, UC_tablas, control_tablas):
        self.CD_tables = pd.read_csv(CD_tablas).set_index(["Unnamed: 0"]).T
        self.UC_tablas = pd.read_csv(UC_tablas).set_index(["Unnamed: 0"]).T
        self.control_tables = pd.read_csv(control_tablas).set_index(["Unnamed: 0"]).T
        self.species_main_MGX = None

    def pull_phenotype(self):
        self.CD_tables["Diagnosis"] = "CD"
        self.UC_tablas["Diagnosis"] = "UC"
        self.control_tables["Diagnosis"] = "Control"
        self.species_main_MGX = pd.concat([self.CD_tables, self.UC_tablas], axis=0, join="outer")
        self.species_main_MGX = pd.concat([self.species_main_MGX, self.control_tables], axis=0, join="outer")

        self.species_main_MGX["Diagnosis"]  = self.species_main_MGX[["Diagnosis"]].fillna('').agg(''.join, axis=1)
        self.species_main_MGX = self.species_main_MGX.T.drop_duplicates(keep='last').T.replace(["",np.NAN], 0)
        self.species_main_MGX = self.species_main_MGX.drop("species_name", axis=1)
        # self.species_main_MGX.to_csv("/Users/odedsabah/Desktop/test10.csv" ,index=True)


    def species_threshold(self):
        self.species_main = self.species_main_MGX.loc[:, (self.species_main_MGX == 0).mean() < 0.8]
        self.species_main.to_csv("/Users/odedsabah/Desktop/MTX.csv")


        # for column in self.species_main_MGX.columns[1:]:
        #     if is_numeric_dtype(self.species_main_MGX[column]):
        #         if sum(self.species_main_MGX[column]) < 1:
        #             self.species_main_MGX.drop([column], axis=1, inplace=True)
        # self.species_main_MGX.to_csv("/Users/odedsabah/Desktop/merge_MGX.csv" ,index=True)


def main():
    if len(sys.argv) != 4:
        quit("\nUsage: " + sys.argv[0] + "CD_tables" + "UC_tables" + "control_tables  \n\n")

    CD_tables = sys.argv[1]
    UC_tables = sys.argv[2]
    control_tables = sys.argv[3]

    M = merging_tables(CD_tablas = CD_tables, UC_tablas = UC_tables, control_tablas= control_tables)
    M.pull_phenotype()
    M.species_threshold()
if __name__ == '__main__':
    main()



