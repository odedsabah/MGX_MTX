import pandas as pd
import os
import sys


class Metaphlane3_abundance:

    def __init__(self,Path_MGX_MP):
        self.Path_MGX_MP_CD = Path_MGX_MP
        self.Name_Hierarchical = None
        self.dict_Hierarchical = dict()

    def get_data(self):
        '''
        This function reads the information from a metaphlan file and stores it in two lists (bacteria_name, percent_list)
        '''
        samples = [x for x in os.listdir(self.Path_MGX_MP_CD) if x.endswith(".txt")]
        for sample in samples:
            with open(f'{self.Path_MGX_MP_CD}/{sample}') as s:
                f = s.readlines()
            for line in f:
                #k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Lachnospiraceae|g__Coprococcus|s__Coprococcus_comes 2|1239|186801|186802|186803|33042|410072        0.00264
                split_line = line.strip().split()[0]
                key = split_line.split('|')[-1]
                self.dict_Hierarchical[key] = split_line
        self.Name_Hierarchical = pd.DataFrame.from_dict(self.dict_Hierarchical,orient='index')
        self.Name_Hierarchical.to_csv("~/Metaphlan4_prediction/Metaphlan4_set_species_control.csv")

def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + "Path_MGX_MP \n\n")

    Path_MGX_MP = sys.argv[1]

    M_A = Metaphlane3_abundance(Path_MGX_MP)
    M_A.get_data()

if __name__ == '__main__':
    main()


