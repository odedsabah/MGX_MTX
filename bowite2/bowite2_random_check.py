#!/usr/bin/python3

# This program takes an MT / GX fasta file that matches the same sample and then randomly samples 40
# of the samples and builds the references with the MGX (Bowite2 -build) and the MTX maps and checks the coverage.
# input: fasta file of MT/GX
# output: BAM file for each sample

# Upload packages
import pandas as pd
import sys
import os
import subprocess
import random
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE
from pathlib import Path
from tempfile import TemporaryDirectory

if len(sys.argv) != 4:
    quit("\nUsage: " + sys.argv[0] + " <path_MGX_fasta_file> + <path_MTX_fasta_file> + <path_esco_index> + <output_directory> \n\n")

path_MGX_fasta_file = sys.argv[1]
path_MTX_fasta_file = sys.argv[2] # directory containing fastq.gz files
path_esco_index = sys.argv[2] # options
output_directory = sys.argv[3]

# import data
metadata = pd.read_csv("/home/odeds/hmp2_metadata.csv")

# select columns relevant
df = metadata.loc[:,["External ID", "Participant ID", "data_type","date_of_receipt"]]

gro = df.groupby(["External ID" ,"Participant ID","date_of_receipt"])["data_type"].apply(list)

# display all file with match
def f(t_p):
      return "metagenomics" and "metatranscriptomics" in t_p
c = gro.apply(f)

# Choose random 40 samples
random_40 = (c[c].sample(40))
R_40 = (pd.DataFrame(random_40))

#c[c].to_csv("/Users/odedsabah/Desktop/hmp.csv") #output for local

# Check whether the specified directory exists, if already exist quit
if os.path.isdir(output_directory) == True:
    quit("directory already exists: " + output_directory)

# Create the output directory. If the function fails - quit
os.mkdir(output_directory)

# Create the directory bt2 under the output directory
bt2_dir = output_directory + "/bt2"
os.mkdir(bt2_dir)

def read_map(fna: Path, reads: Path, output: Path, num_threads: int):
    """
    Using bowtie2, shrinksam and samtools, creates a sorted and indexed bam file.
    The file is written into the given output path.
    Logs are not kept.
    Clean ups after self.
    """
    with TemporaryDirectory() as work_dir:
        steps = [f'bowtie2-build -f {fna.as_posix()} {work_dir}/bt2db',
                 f'bowtie2 -p {num_threads} --very-sensitive -x {work_dir}/bt2db -U {reads.as_posix()} 2> {output.as_posix()}.log | shrinksam > {work_dir}/unsorted.bam',
                 f'samtools sort {work_dir}/unsorted.bam > {output.as_posix()}',
                 f'samtools index {output.as_posix()}']
        for step in steps:
            p = Popen(step, shell=True,
                      stderr=PIPE,
                      stdout=PIPE)
            p.wait()


def bowite2_index (R_40, path_MGX_fasta_file, path_MTX_fasta_file):
    fasta_base_path = Path(path_MGX_fasta_file)
    reads_base_path = Path(path_MTX_fasta_file)
    phenotypes = ('CD', 'control', 'UC')
    for sample in R_40.index:
        for pheno in phenotypes:
            sample_fasta = fasta_base_path / pheno / 'assembly.d' / sample[0] / '2.post-assembly' / 'assembly.min500.fna'
            if sample_fasta.is_file():
                break
        sample_reads = reads_base_path / f'{sample[0]}.fastq.gz'
        if sample_fasta.is_file() and sample_reads.is_file():
            print(sample[0])
            read_map(fna=sample_fasta,
                     reads=sample_reads,
                     output=Path(f'/home/odeds/bt_40/{sample[0]}.{pheno}.sorted.bam'),
                     num_threads=60)
        else:
            print(f'Sample {sample[0]} not found, looking in  {sample_fasta} and {sample_reads}')


                    #     #bowtie2-build bt2/CSM79HGP.assembly.fna bt2/CSM79HGP.assembly.fna >bt2/CSM79HGP.assembly.fna.stdout 2> bt2/CSM79HGP.assembly.fna.stderr
                    #     bt2_dir = subprocess.Popen(["bowtie2-build", path_MGX_fasta_file + "/" + sample[0] + "/2.post-assembly/assembly.min500.fna", "/home/odeds/bt_40/bt2/db_bt" , ">", path_MGX_fasta_file, sample[0] + "/2.post-assembly/assembly.min500.fna", ".assembly.fna.stdout", "2>" + path_MGX_fasta_file, sample[0] + "/2.post-assembly/assembly.min500.fna", ".assembly.fna.stderr"])
                    #     bt2_dir = subprocess.call(["bowtie2-build", os.path.join(path_MGX_fasta_file, sample[0], "/2.post-assembly/assembly.min500.fna"), os.path.join(">", path_MGX_fasta_file, sample[0], "/2.post-assembly/assembly.min500.fna", ".assembly.fna.stdout"), os.path.join("2>", path_MGX_fasta_file, sample[0], "/2.post-assembly/assembly.min500.fna", ".assembly.fna.stderr")])
                    #     print(bt2_dir)
                    #     bt2_dir.wait()
                    #
                    #     bowtie2 -x bt2/CSM79HGP.assembly.fna -U /data1/Human/ibdmdb2/metatranscriptomics/raw.d/CSM79HGP.fastq.gz -p 30 --very-sensitive --no-head --no-unal -S mtx.vs.CSM79HGP.assembly.fna.sam 2> mtx.vs.CSM79HGP.assembly.fna.sam.stderr
                    #     bowtie2 -x bt2/CSM79HGP.assembly.fna -U /data1/Human/ibdmdb2/metatranscriptomics/raw.d/CSM79HGP.fastq.gz -p 30 --very-sensitive --no-head --no-unal -S mtx.vs.CSM79HGP.assembly.fna.sam 2> mtx.vs.CSM79HGP.assembly.fna.sam.stderr
                    #     R_bt2 = subprocess.Popen(["bowtie2 -x " + "/home/odeds/bt_40/bt2/db_bt" + " -U " + path_MTX_fasta_file + "/" + sample[0] + "--very-sensitive -p 60  " + "--no-head --no-unal ", "-o" + "/home/odeds/bt_40/db_bt/" + sample[0] + ".sam"])
                    #     print(R_bt2)
                    # except:
                    #     print(sample[0] + "it's not found")

bowite2_index( R_40 ,path_MGX_fasta_file, path_MTX_fasta_file)




