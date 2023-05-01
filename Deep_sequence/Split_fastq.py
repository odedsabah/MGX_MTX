#!/usr/bin/python3

import sys
import gzip

def prepare_fastq_file(fastq_file, fout_list, jump, num_reads):
    with gzip.open(fastq_file, "rt") as fin:
        for i, line in enumerate(fin):
            line += fin.readline()
            line += fin.readline()
            line += fin.readline()
            group = i % 10
            print(group)
            if (i - group) % jump == 0:
                print(i, group, line)
                fout_list[group].write(line)
            elif i / 4 == num_reads:
                break
def main():

    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <path_file_metaphlan_file> \n\n")

    Path_MP4_files = sys.argv[1]

    # Define the input and output file paths
    input_file = Path_MP4_files
    output_files = [f"group_{i}.fastq.gz" for i in range(0, 10)]

    # Define the number of reads to select and the jump value
    num_reads = 1e6
    jump = 180

    # Open all output files at the beginning
    fout_list = [gzip.open(output_file, "wt") for output_file in output_files]

    # Split the fastq file into 10 groups of 1 million reads each
    for i in range(10):
        # Select the sequences for the group and write them to the output files
        prepare_fastq_file(input_file, fout_list, jump, num_reads)

    # Close all output files
    for fout in fout_list:
        fout.close()

if __name__ == '__main__':
    main()


