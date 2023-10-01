import pandas as pd
import os
import sys


class Metaphlane4_abundance:

    def __init__(self, path_MGX_MP):
        self.path_MGX_MP_CD = path_MGX_MP
        self.name_hierarchical = None
        self.dict_hierarchical = dict()
        self.all_data = dict()
        self.id_files = set()

    def get_data(self):
        samples = [x for x in os.listdir(self.path_MGX_MP_CD) if x.endswith(".txt")]

        for sample in samples:
            id_file = sample.split('.')[0]
            self.id_files.add(id_file)

            with open(f'{self.path_MGX_MP_CD}/{sample}') as s:
                f = s.readlines()

            for line in f:
                split_line = line.strip().split()[0]
                key = split_line.split('|')[-1]
                self.dict_hierarchical[key] = split_line
                self.all_data[key] = split_line

        self.name_hierarchical = pd.DataFrame.from_dict(self.dict_hierarchical, orient='index')
        return self.name_hierarchical

    def sankey_plot(self):
        # Convert split data into dataframe
        rows = [value.split('|') for value in self.all_data.values()]
        col_names = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species', 'Strain']
        df_sankey_plot = pd.DataFrame(rows, columns=col_names)
        print(df_sankey_plot)
        # return df_sankey_plot

def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <Path_MGX_MP>\n\n")

    Path_MGX_MP = sys.argv[1]

    M_A = Metaphlane4_abundance(Path_MGX_MP)
    hierarchical_data = M_A.get_data()
    sankey_data = M_A.sankey_plot()

if __name__ == '__main__':
    main()




