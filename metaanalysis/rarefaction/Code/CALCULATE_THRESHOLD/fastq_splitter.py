#!/usr/bin/python3

import gzip
import pandas as pd
import os
import math
import concurrent.futures


class FastqSplitter:
    def __init__(self, fastq_path, read_stats):
        self.fastq_path = fastq_path
        self.read_stats = read_stats

    @staticmethod
    def prepare_fastq_file(fastq_file, fout_list, jump, sample_size, max_groups):
        with gzip.open(fastq_file, "rt") as fin:
            for i, line in enumerate(fin):
                line += fin.readline()
                line += fin.readline()
                line += fin.readline()
                group = i % max_groups
                if (i - group) % jump == 0:
                    fout_list[group].write(line)
                    if i == sample_size:
                        break

    @staticmethod
    def cal_sample_size(read_stats, fastq_file):
        id_file = fastq_file.split('/')[-2]
        df_size = pd.read_csv(read_stats, delimiter='\t', skiprows=1)
        size_by_id = df_size[df_size.iloc[:, 0].str.startswith(id_file)]
        sample_size = int(size_by_id.iloc[:, 3])
        sample_size = math.floor(sample_size / 1e7) * 1e7
        return sample_size, id_file

    @staticmethod
    def run_metaphlan(fastq_file_out, metaphlan_file_out):
        os.system(f'/data1/software/metaphlan/run-metaphlan.sh {fastq_file_out} {metaphlan_file_out}'
                  f' 40 > {metaphlan_file_out}.stdout')

    def split(self):
        sample_size, id_file = self.cal_sample_size(self.read_stats, self.fastq_path)
        num_reads = 0
        max_groups = 10

        # Create output directory if it doesn't exist
        output_dir = f"mp4.split_.{id_file}"
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        processed_files = []

        while True:
            num_reads += 1e6
            fout_list = []
            new_files = []
            for i in range(0, max_groups):
                output_file = f"{output_dir}/{id_file}.{int(num_reads // 1e6)}M_group_{i + 1}.fastq.gz"
                fout_list.append(gzip.open(output_file, "wt"))
                new_files.append(output_file)

            jump = int(sample_size / num_reads)
            if jump < max_groups:
                break

            self.prepare_fastq_file(self.fastq_path, fout_list, jump, sample_size, max_groups)

            # Run metaphlan on new files only
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(0, max_groups):
                    if new_files[i] not in processed_files:
                        fastq_file_out = new_files[i]
                        metaphlan_file_out = f"{output_dir}/{id_file}.{int(num_reads // 1e6)}M_group_{i + 1}.txt"
                        executor.submit(self.run_metaphlan, fastq_file_out, metaphlan_file_out)
                        processed_files.append(new_files[i])

            for fout in fout_list:
                fout.close()

        return id_file
