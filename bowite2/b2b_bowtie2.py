#!/usr/bin/python3
# This program takes as an input fastq.zip files and fasta file
# the output is a sam file for each fastq file built by bowtie2build and bowtie2

import sys
import os
import subprocess
import random
from os import listdir
from os.path import isfile, join

if len(sys.argv) != 5:
    quit("\nUsage: " + sys.argv[0] + " <path_MGX_fasta_file> + <path_MTX_fasta_file> + <samples_amount_of_random_choice> + <output_directory>\n\n")


path_MGX_fasta_file = sys.argv[1]
path_MTX_fasta_file = sys.argv[2] # directory conataning fastq.gz files
random_choice = sys.argv[3]
output_directory = sys.argv[4]


onlyfiles = [f for f in listdir(path_MGX_fasta_file) if isfile(join(path_MGX_fasta_file, f))]

def match_samples (path_MGX_fasta_file, path_MTX_fasta_file):
    for sample in samples:
        random.choice(path_MGX_fasta_file, 40)


# Check whether the specified directory exists, if already exist quit
if os.path.isdir(output_directory) == True:
    quit("directory already exists: " + output_directory)

# Create the output directory. If the function fails - quit
os.mkdir(output_directory)

# Create the directory bt2 under the output directory
bt2_dir = output_directory + "/bt2"
os.mkdir(bt2_dir)

# Create the bowtie2 index database using bowtie2-build
# database will be stored under the bt2 directory
# command line: bowtie2-build ../rpS3.fna rpS3.fna --threads 40
bt2_db = bt2_dir + "/" + path_MGX_fasta_file[path_MGX_fasta_file.rfind("/") +1:]
p = subprocess.Popen(["bowtie2-build", "-q" , path_MGX_fasta_file, bt2_db])
p.wait()

# bowtie
for root, dirs, files in os.walk(fastq_directory):
    if (root == fastq_directory) or root.endswith('fastqc') or (root.find('all') != -1) or (root.find('both') != -1) or (root.find('temp') != -1):
        continue
    name_of_sample = root[root.rfind("/")+1:]
    list_of_files = []
    for name in files:
        if name.endswith((".fastq.gz")):
            list_of_files.append(os.path.join(root, name))
    pairs_str = ",".join(list_of_files)
    cmd = "bowtie2 -x " + bt2_db + " -U " + pairs_str + " --very-sensitive -p 60 -S " + output_directory + "/" + name_of_sample + "_hits.sam"
    os.system(cmd)