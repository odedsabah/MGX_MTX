#!/usr/bin/python3

# Upload packages
import sys
import gzip
import os


'''selected_reads(sample_size) is a function that returns a list of the number of reads to
select at different sequencing depths, based on an input sample_size'''

def selected_reads(sample_size):
    n_serial = (list(range(1, 9)) + list(range(10, 18, 2)) + list(range(20, 49, 5)) + list(range(50, 99, 10)) +
                list(range(100, 999, 100)) + list(range(1000, 10001, 1000)))
    n_serial = [i * 1e6 for i in n_serial]
    selected_read = [sample_size // i for i in [i for i in n_serial]]
    dict_selected_read = dict(zip(n_serial, selected_read))
    return dict_selected_read

def prepare_fastq_file(fastq_file, fastq_file_out, jump, num_reads):
    with gzip.open(fastq_file, "rt") as fin, gzip.open(fastq_file_out, "wt") as fout:
        counter = 0
        for line in fin:
            line += fin.readline()
            line += fin.readline()
            line += fin.readline()
            counter += 1
            if counter % jump == 0:
                fout.write(line)
                if counter // jump == num_reads:
                    break

def main():

    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <path_fastq_file> \n\n")

    fastq_file = sys.argv[1]

    sample_size = 258e6
    dict_selected_read = selected_reads(sample_size)

    if not os.path.isdir(f"mp4.depth_.{fastq_file.split('/')[5]}"):
        os.mkdir(f"mp4.depth_.{fastq_file.split('/')[5]}")
    id_file = f"mp4.depth_.{fastq_file.split('/')[5]}/" + fastq_file.split('/')[5]
    for i, (num_reads, jump) in enumerate(dict_selected_read.items()):
        fastq_file_out = f"{id_file}.{int(num_reads // 1e6)}M.fastq.gz"
        metaphlan_file_out = f"{id_file}.{int(num_reads // 1e6)}M.txt"
        prepare_fastq_file(fastq_file, fastq_file_out, jump, num_reads)
        os.system(f'/data1/software/metaphlan/run-metaphlan.sh {fastq_file_out} {metaphlan_file_out}'
                  f' 40 > {metaphlan_file_out}.stdout')
        os.system(f"rm -f {fastq_file_out}")

if __name__ == '__main__':
    main()
