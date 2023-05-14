#!/usr/bin/python3

import sys
import gzip
import pandas as pd
import math

def prepare_fastq_file(fastq_file, fout_list, jump, sample_size):
    with gzip.open(fastq_file, "rt") as fin:
        for i, line in enumerate(fin):
            line += fin.readline()
            line += fin.readline()
            line += fin.readline()
            group = i % 10
            if (i - group) % jump == 0:
                fout_list[group].write(line)
                if i == sample_size:
                    break

def cal_sample_size(read_stats,fastq_file):
    id = fastq_file.split('/')[5]
    df_size = pd.read_csv(read_stats, delimiter='\t', skiprows=1)
    size_by_id = df_size[df_size.iloc[:, 0].str.startswith(id)]
    sample_size = int(size_by_id.iloc[:, 3])
    sample_size = math.floor(sample_size / 1e7) * 1e7
    return sample_size, id

def main():

    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + " <Path_MP4_files> <Read_stats> \n\n")

    Path_MP4_files = sys.argv[1]
    Read_stats = sys.argv[2]
    input_file = Path_MP4_files
    # Define the input and output file paths
    sample_size, id = cal_sample_size(Read_stats, Path_MP4_files)
    num_reads = 0
    while True:
        num_reads += 1e6
        output_files = [f"{id}_group_{i+1}-{int(num_reads//1e6)}M.fastq.gz" for i in range(0, 10)]

        # Define the number of reads to select and the jump value
        jump = int(sample_size / num_reads)
        if jump <= 1:
            break

        # Open all output files at the beginning
        fout_list = [gzip.open(output_file, "wt") for output_file in output_files]

        # Split the fastq file into 10 groups of 1 million reads each
        # Select the sequences for the group and write them to the output files
        prepare_fastq_file(input_file, fout_list, jump, sample_size)

        # Close all output files
        for fout in fout_list:
            fout.close()

        if not os.path.isdir("mp4.Split"):
            os.mkdir("mp4.Split")
        for path_file, id_file in zip(file_paths, id_files):
            metaphlan_file_out = f"{id_file}.txt"
            os.system(f'/data1/software/metaphlan/run-metaphlan.sh {path_file} ~/metaanalysis/mp4.simulation/{metaphlan_file_out}'
                      f' 40 > ~/metaanalysis/mp4.simulation/{metaphlan_file_out}.stdout')
if __name__ == '__main__':
    main()



