#!/usr/bin/python3

import sys
import os
import glob
from pathlib import PurePosixPath
from tempfile import TemporaryDirectory

if len(sys.argv) != 3:
    quit("\nUsage: " + sys.argv[0] + " <path_of_bt2_40> + <path_MTX_fasta_file> + <path_esco_index> + <output_directory> \n\n")

path_of_bt2_40 = sys.argv[1]
path_MTX_fasta_file = sys.argv[2]

class match_esco_vs_MTX:

    def __init__(self, path, path_MTX):
        self.path = path
        self.path_MTX = path_MTX

    def p40 (self):
        self.path = path_of_bt2_40
        for filename in os.listdir(path_of_bt2_40):
            if filename.endswith(".log"):
                n_sample = filename.split(".")
                name2phenotypes[n_sample[0]] = n_sample[1]
                print(name2phenotypes)

    def esco_vs_MTX (self):
        self.path_MTX = path_MTX_fasta_file
        # for kay, index in :
        #     for trans in os.walk(path_MTX_fasta_file):
        #         print(trans)


#match_esco_vs_MTX(path=path_of_bt2_40, path_MTX=path_MTX_fasta_file)

MEVS = match_esco_vs_MTX
print(MEVS.__init__(self=MEVS ,path=path_of_bt2_40, path_MTX=path_MTX_fasta_file ))

# def read_map(fna: Path, reads: Path, output: Path, num_threads: int):
#     """
#     Using bowtie2, shrinksam and samtools, creates a sorted and indexed bam file.
#     The file is written into the given output path.
#     Logs are not kept.
#     Clean ups after self.
#     """
#     with TemporaryDirectory() as work_dir:
#         steps = [f'bowtie2-build -f {fna.as_posix()} {work_dir}/bt2db',
#                  f'bowtie2 -p {num_threads} --very-sensitive -x {work_dir}/bt2db -U {reads.as_posix()} 2> {output.as_posix()}.log | shrinksam > {work_dir}/unsorted.bam',
#                  f'samtools sort {work_dir}/unsorted.bam > {output.as_posix()}',
#                  f'samtools index {output.as_posix()}']
#         for step in steps:
#             p = Popen(step, shell=True,
#                       stderr=PIPE,
#                       stdout=PIPE)
#             p.wait()



        #     sample_fasta = fasta_base_path / pheno / 'assembly.d' / sample[0] / '2.post-assembly' / 'assembly.min500.fna'
        #     if sample_fasta.is_file():
        #         break
        # sample_reads = reads_base_path / f'{sample[0]}.fastq.gz'
        # if sample_fasta.is_file() and sample_reads.is_file():
        #     print(sample[0])
        #     read_map(fna=sample_fasta,
        #              reads=sample_reads,
        #              output=Path(f'/home/odeds/bt_40/{sample[0]}.{pheno}.sorted.bam'),
        #              num_threads=60)
        # else:
        #     print(f'Sample {sample[0]} not found, looking in  {sample_fasta} and {sample_reads}')

