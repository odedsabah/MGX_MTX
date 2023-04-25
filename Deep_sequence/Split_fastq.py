#!/usr/bin/python3

# Import packages
import sys
import gzip


def prepare_fastq_file(fastq_file, fastq_file_out, jump, num_reads, start_read):
    with gzip.open(fastq_file, "rt") as fin, gzip.open(fastq_file_out, "wt") as fout:
        counter = 0
        sequence_counter = 0
        dictionary = {}
        for i, line in enumerate(fin):
            line += fin.readline()
            line += fin.readline()
            line += fin.readline()
            counter += 1
            sequence_counter += 1
            if start_read <= counter <= start_read + num_reads - 1 and (counter - start_read) % jump == 0:
                print(start_read,counter, start_read + num_reads - 1, jump)
                fout.write(line)
            elif counter // jump == num_reads:
                break
            else:
                dictionary[counter] = line
        if dictionary:
            with open(fastq_file_out, "wt") as fout:
                for key in sorted(dictionary.keys()):
                    fout.write(dictionary[key])

def main():

    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <path_file_metaphlan_file> \n\n")

    Path_MP4_files = sys.argv[1]

    # Define the input and output file paths
    input_file = Path_MP4_files
    output_files = [f"group_{i}.fastq.gz" for i in range(1, 11)]

    # Define the number of reads to select and the jump value
    num_reads = 1e6
    jump = 180

    # Split the fastq file into 10 groups of 1 million reads each
    for i, output_file in enumerate(output_files):
        # # Calculate the number of sequences to select for the group
        num_sequences = int(num_reads / jump)
        # Calculate the starting read number for the group
        start_read = i + jump
        print(start_read)
        # Select the sequences for the group and write them to the output file
        prepare_fastq_file(input_file, output_file, jump, num_sequences, start_read)

if __name__ == '__main__':
    main()