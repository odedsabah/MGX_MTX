#3!/usr/bin/python3


# Upload packages
import sys
import pandas as pd

#---
#date: "5/4/2022"
#input:  Ready Df for analysis Coverage MG/TX
#output: DF with distances from the start to and in per contigs
#---

# MGX_coverage_stats = '/Users/odedsabah/Desktop/CSM79HGP.MGX.coverage-stats.txt'
# MTX_coverage_stats = '/Users/odedsabah/Desktop/CSM79HGP.MTX.coverage-stats.txt'
# gff_file = '/Users/odedsabah/Desktop/CSM79HGP.gff'
# min_length = 900
# max_length = 1100

if len(sys.argv) != 6:
        quit("\nUsage: " + sys.argv[0] + " <MGX-coverage-stats> <gff-file> <min-length> <max_length> \n")


MGX_coverage_stats = sys.argv[1]  #The input (MGX_coverage_stats) is output of cal_dist.py in test3
MTX_coverage_stats = sys.argv[2]
gff_file = sys.argv[3]
min_length = sys.argv[4]
max_length = sys.argv[5]

valid_contigs = []
with open(gff_file) as fin:
    for line in fin:
        # k119_47955    Prodigal_v2.6.3 CDS     12678   13244   102.5   +       0       ID=1_9;partial=00;start_type=ATG;rbs_motif=None;rbs_spacer=None;gc_cont=0.568;conf=100.00;score=101.87>
        fs = line.strip().split("\t")
        if line[0] == "#" or fs[2] != "CDS":
            continue
        try:
            (contig_length, length_read) = fs[0], (int(fs[4]) - (int(fs[3])))
            if min_length <= int(length_read) <= max_length:
                valid_contigs.append(contig_length)
        except:
            quit("Unexpected line: " + line)


def MGX_C2_DF (MGX_coverage_stats, MTX_coverage_stats):
    MGX_DF = pd.read_csv(MGX_coverage_stats, sep='\t')
    # Contig Start	End	Median	Mean Sd	Min-cvg	Max-cvg	cvg.start+10 cvg.end-10
    try:
        MGX_DF = MGX_DF.loc[MGX_DF["Contig"].isin(valid_contigs), :]
        MGX_DF["Start_200"] = MGX_DF["Start"] + 200
        MGX_DF["End_300"] = MGX_DF["End"] - 300
        MGX_DF["End_100"] = MGX_DF["End"] - 100
        MGX_DF = MGX_DF.loc[:, ("Contig", "Start", "Start_200", "End_300", "End_100", "End")]

        print(MGX_DF)

    except:
        print("Unexpected : " + MGX_DF["Contig"])

    try:
        MTX_DF = pd.read_csv(MTX_coverage_stats, sep='\t')
        # Contig Start	End	Median	Mean Sd	Min-cvg	Max-cvg	cvg.start+10 cvg.end-10
        MTX_DF = MTX_DF.loc[MTX_DF["Contig"].isin(valid_contigs), :]
        MTX_DF["Start_200"] = MTX_DF["Start"] + 200
        MTX_DF["End_300"] = MTX_DF["End"] - 300
        MTX_DF["End_100"] = MTX_DF["End"] - 100
        MTX_DF = MTX_DF.loc[:, ("Contig", "Start", "Start_200", "End_300", "End_100", "End")]

        print(MTX_DF)
        # MGX_DF.to_csv("/Users/odedsabah/Desktop/out_test.tsv", sep='\t', index= False)
    except:
        print("Unexpected : " + MTX_DF["Contig"])

if __name__ == '__main__':
    print(MGX_C2_DF(MGX_coverage_stats, MTX_coverage_stats))





