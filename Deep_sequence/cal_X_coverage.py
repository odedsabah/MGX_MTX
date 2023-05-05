#!/usr/bin/python3

import sys
import os
import gzip
import pandas as pd


def Get_id(fastq_file):
    # list the files in the fastq_file directory and filter for .fastq.gz files
    files_list = [file for file in os.listdir(fastq_file) if file.endswith('.fastq.gz')]
    # create a list of file paths and id_file values using list comprehension
    file_paths = [os.path.join(fastq_file, file_name) for file_name in files_list]
    id_files = [f'{file_name.split("_")[3]}_Coverage' for file_name in files_list]
    # return a tuple with the lists of file paths and id_file values
    # print(file_paths, id_files)
    return file_paths, id_files

def Create_ref (Taxa_list_ref):
    Taxa_list_ref = pd.read_csv(Taxa_list_ref, header= None, delimiter='\t')
    Taxa_list_ref['Species'] = 's__' + Taxa_list_ref.iloc[:,0].str.split().str[:2].str.join("_")
    Taxa_list_ref['Abundance'] = 10
    Taxa_list_ref = Taxa_list_ref.iloc[:, 1:].set_index('Species')
    return Taxa_list_ref

def main():

    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + " <path_fastq_file_X_cov> <Taxa_list_ref> \n\n")

    path_fastq_file_X_cov = sys.argv[1]
    Taxa_list_ref = sys.argv[2]

    file_paths, id_files = Get_id(path_fastq_file_X_cov)
    Create_ref(Taxa_list_ref)

    if not os.path.isdir("mp4.Simulation"):
        os.mkdir("mp4.simulation")
    for path_file, id_file in zip(file_paths, id_files):
        metaphlan_file_out = f"{id_file}.txt"
        os.system(f'/data1/software/metaphlan/run-metaphlan.sh {path_file} ~/metaanalysis/mp4.simulation/{metaphlan_file_out}'
                  f' 40 > ~/metaanalysis/mp4.simulation/{metaphlan_file_out}.stdout')

if __name__ == '__main__':
    main()