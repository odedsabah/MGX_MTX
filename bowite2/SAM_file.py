#!/usr/bin/python3

# this programme takes a sam file and the name of a sequence as an input and filters all data exept names of sequences
# input: sam file and the name of a sequence
# output: list of names of sequences in a txt file

import sys
from os import write
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

seq_name_find = 'k119_6766'  # input("Enter seq name:")
sam_file = '/Users/odedsabah/Desktop/SAM_test.txt'  # input("Enter location SAM file:")
fasta_file = '/Users/odedsabah/Desktop/fasta_file_exam.txt'  # input("Enter location fasta(references) file:")

'''if len(sys.argv) != 4:
   quit("\nUsage: " + sys.argv[0] + " <seq_name_find> <sam_file> <fasta_file>\n\n") # sys.argv[0]-The name of new fill

script_name = sys.argv[0]
seq_name_find = sys.argv[1]
sam_file = sys.argv[2]
fasta_file = sys.argv[3]'''

seq2n_reads = {}  # Create a dictionary that contains the sequence names and amount
with open(sam_file) as sf:  # open the file and alias to sf
    for line in sf:
        if len(line.strip()) == 0:  # skip empty rows
            continue  # continue empty line
        split_arg = line.strip().split("\t")
        if int(split_arg[1]) & 4 == 0:
            try:
                seq = split_arg[2]  # the name of the seq in sam file
                seq2n_reads[seq] = seq2n_reads.get(seq, 0) + 1
            except:
                quit("error happened in sam file: " + line)

'''# This faction is the same as fasta2read with package Bio.SeqIO
record_dict = IO.to_dict(IO.parse('/Users/odedsabah/Desktop/fasta_file_exam.txt', "fasta"))
for key in record_dict.items():
    print(key[0], + len(key[1].seq))'''

fasta2read = {}  # Create a dictionary that contains the sequence names and its length
with open(fasta_file, "r") as file:  # read fasta file
    for line in file:
        try:
            if len(line.strip()) == 0:  # skip empty rows
                continue  # continue empty line
            line = line.strip()  # connection lines
            if line[0] == ">":  # Each new source sequence starts at ">name"
                header = line[1:line.find(" ")]  #
                fasta2read[header] = 0
            else:
                fasta2read[header] += len(line.strip())
        except:
            quit("error happened in fasta file: " + line)
for k in fasta2read.keys():
    split_name_seq = k.split(" ")
    #print(f"{split_name_seq[0]}\t{(fasta2read[k])}") # display the name & length of the reference sequence

#for (seq, n_reads) in seq2n_reads.items():
    #print(seq, n_reads, sep="\t")

for name, n_reads in seq2n_reads.items():
    if name in fasta2read.keys():
            print(name,fasta2read[name], n_reads / fasta2read[name], n_reads, sep="\t")

x = '''GCACTGTTCCTCACGAGCTGCTGCTGTAAATGCAAAGGAGCAGCTTTCCAGGCAGCTTTCGACACGCGTTTCACATCGGCACTCGATGCAGCGCT'''

y = '''GCAAATGCAAACGGAGCAGCTTTCCAGGCAGCTTTCGACACGCGTTTCACATCGGCACTCGATGCAGCGCT'''
alignment = pairwise2.align.globalxx(split_arg[9], y)
print(format_alignment(*alignment[0]))
