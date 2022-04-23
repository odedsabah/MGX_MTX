#!/usr/bin/python3
import sys
from Bio import SeqIO
import numpy as np
import os


if len(sys.argv) != 8:
        quit("\nUsage: " + sys.argv[0] + " <genomic-file> <gff-file> <bam-file> <mgx-coverage-file>e <enter_min_len> <enter_max_len> <out-prefix>\n")

genomic_file = sys.argv[1]
gff_file = sys.argv[2]
bam_file = sys.argv[3]
mgx_coverage_file = sys.argv[4]
min_length = sys.argv[5]
max_length = sys.argv[6]
out_prefix = sys.argv[7]

contig2mgx_coverage = {}

with open(mgx_coverage_file) as fin:
        #rname  startpos        endpos  numreads        covbases        coverage        meandepth       meanbaseq       meanmapq
        fin.readline()
        for line in fin:
                # k119_47955    1       483363  625041  421162  87.1316 119.633 35.8    41.2
                fs = line.strip().split("\t")
                contig2mgx_coverage[fs[0]] = float(fs[5])

contig2positions = {}
for record in SeqIO.parse(genomic_file, "fasta"):
        contig2positions[record.id] = np.zeros(len(record.seq)+1)

###os.system("samtools depth " + bam_file + " -o " + out_prefix + ".depth.txt")

with open(out_prefix + ".depth.txt") as fin:
        for line in fin:
                (contig, pos, cov) = line.strip().split("\t")
                try:
                        contig2positions[contig][int(pos)] = int(cov)
                except:
                        print("Failed to set position", pos, "on contig", contig, "to", cov)
                        print(line)
#                       print("Length of", contig, "is", len(contig2positions[contig]))
                        quit()
with open(gff_file) as fin:
        for line in fin:
                # k119_47955    Prodigal_v2.6.3 CDS     12678   13244   102.5   +       0       ID=1_9;partial=00;start_type=ATG;rbs_motif=None;rbs_spacer=None;gc_cont=0.568;conf=100.00;score=101.87>
                fs = line.strip().split("\t")
                if line[0] == "#" or fs[2] != "CDS":
                        continue
                try:
                        (contig, start, end, strand) = (fs[0], int(fs[3]), int(fs[4]), fs[6])
                except:
                        quit("Unexpected line: " + line)
                if (end-start+1 >= min_length) and (end-start+1 <= max_length):
                        (startc, endc) = (end-10, start+10) if strand == '-' else (start+10, end-10)
                        print(contig, start, end, contig2positions[contig][startc+10]/contig2mgx_coverage[contig], contig2positions[contig][endc-10]/contig2mgx_coverage[contig], sep="\t")


