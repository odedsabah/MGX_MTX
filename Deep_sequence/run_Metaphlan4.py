#!/usr/bin/python3

import sys
import os


def id_files(path_fastq_file):
    path_id = {}
    samples = [x for x in os.listdir(path_fastq_file) if x.endswith(".gz")]
    for sample in samples:
        id_sample = sample.split("_")[-1].split(".")[0]
        path_sample = os.path.join(path_fastq_file, sample)
        path_id[id_sample] = path_sample
    return path_id


def main():
    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <Path_MP4_files> \n\n")

    path_MP4_files = sys.argv[1]

    path_id = id_files(path_MP4_files)
    if not os.path.isdir(f'{path_MP4_files}/mp4_out.SAMEA110452924'):
        os.mkdir(f'{path_MP4_files}/mp4_out.SAMEA110452924')
    for id_file, path_file in path_id.items():
        metaphlan_file_out = f"/data1/Oded.Sabah/metaanalysis/split_SAMEA110452924/mp4_out.SAMEA110452924/{id_file}.txt"
        cmd = f'/data1/software/metaphlan/run-metaphlan.sh {path_file} {metaphlan_file_out} 40 > {metaphlan_file_out}.stdout'
        os.system(cmd)

if __name__ == '__main__':
    main()
