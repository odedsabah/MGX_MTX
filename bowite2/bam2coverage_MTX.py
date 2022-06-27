#!/usr/bin/python3


import pathlib
import sys
import os
from pathlib import Path


if len(sys.argv) != 2:
    quit("\nUsage: " + sys.argv[0] + " <path_MTX_BAM_file>  \n\n")

path_MTX_BAM_file = sys.argv[1]

def bam2coverage(BAM_f):
    global sample
    BAM_f = Path(path_MTX_BAM_file)
    samples = sorted(BAM_f.glob("*.bam"))
    for sample in samples:
        print(sample)
        coverages = os.system(f'samtools depth {sample} > {sample}.sorted.coverage')

bam2coverage(path_MTX_BAM_file)


