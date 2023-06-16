#!/usr/bin/python3

# Upload packages
import os
import pandas as pd

'''
The script expects one command-line argument as input:

1. `path_file_metaphlan_file`: The path to the directory containing Metaphlan output files.

When executing the script from the command line, you would provide this argument. Here's an example:

<python Stat_from_select.py /path/to/metaphlan_output_directory>

As for the output, the script generates a CSV file named "Taxa_stats_{id_file}_tresh_{Threshold}.csv".
 The file contains the results of the data analysis, including Jaccard similarity scores and Bray-Curtis dissimilarity scores.

The CSV file includes the following columns:
- `Col_name`: The column names representing the samples.
- `Num_of_species`: The number of species in each sample.
- `Ground_truth`: The name of the ground truth sample with the highest numerical value in the column names.
- `Dissimilarity`: The Bray-Curtis dissimilarity scores between each sample and the ground truth sample.
- `l1_score`: The L1 scores (sum of absolute differences) between each sample and the ground truth sample.
- `l2_score`: The L2 scores (Euclidean distances) between each sample and the ground truth sample.

*** Comparison rule versus ground_truth This is a FASTQ file with the maximum number of readings ***

The output CSV file is saved in the same directory as the script.

Please note that the script assumes the presence of Metaphlan output files in the specified directory,
and it expects the files to be in a specific format. Ensure that the directory contains the necessary files for the script to execute successfully.
'''

class MetaphlanAnalysis:
    def __init__(self, path_mp4_files):
        self.path_mp4_files = path_mp4_files

    def get_data(self, threshold):
        species_main = None
        samples = [x for x in os.listdir(self.path_mp4_files) if x.endswith(".txt")]
        for sample in samples:
            species_abundance = dict()
            sample_name = sample[:-4]
            with open(f'{self.path_mp4_files}/{sample_name}.txt') as s:
                f = s.readlines()
                for line in f:
                    if line.startswith("k__Bacteria"):
                        try:
                            species = line.strip().split("\t")[0].split("|")[-1]
                            abundance = float(line.split()[2])
                            if species.startswith('s__') and abundance >= threshold:
                                species_abundance[species] = abundance
                        except:
                            print(f'this value: {line.split()[2]} is not an abundance')
            Taxa_Abundance = pd.DataFrame((species_abundance.items()), columns=['Species',sample_name]).set_index('Species')
            species_main = pd.concat([species_main,Taxa_Abundance], axis=1, join="outer").fillna(0)
        return species_main

    def compute_jaccard_scores(self, df):
        similarity_scores = {}
        ground_truth = max(df.columns, key=lambda x: int(''.join([i for i in x.split('.')[-1] if i.isdigit()])))
        for col in df.columns:
            species1 = df.loc[df[col] > 0, :].index
            species2 = df.loc[df[ground_truth] > 0, :].index
            intersection = len(set(species1).intersection(set(species2)))
            union = len(set(species1).union(set(species2)))
            score = intersection / union
            similarity_scores[col] = score
        Taxa_stats = pd.DataFrame([(col, sum(df[col] > 0 ), similarity_scores[col]) for col in df.columns],
                                  columns=['Col_name', 'Num_of_species', 'Ground_truth']).set_index('Col_name')
        return Taxa_stats, ground_truth

    def compute_bray_curtis_dissimilarity(self, df, Taxa_stats, ground_truth, threshold):
        def distance_calculation(u, v):
            l2 = ((u - v) ** 2).sum() ** 0.5
            l1 = sum(abs(u - v))
            den = sum(u + v)
            distance = l1 / den
            return distance, l1, l2

        u = df[ground_truth]
        dissimilarity_scores = []
        l1_scores = []
        l2_scores = []
        for col in df.columns:
            v = df[col]
            distance, l1, l2 = distance_calculation(u, v)
            dissimilarity_scores.append(distance)
            l1_scores.append(l1)
            l2_scores.append(l2)
        dissimilarity_matrix = pd.DataFrame({'Dissimilarity': dissimilarity_scores, 'l1_score': l1_scores, 'l2_score': l2_scores},
                                            index=df.columns)
        df = pd.concat([Taxa_stats, dissimilarity_matrix], axis=1).reset_index()

        def get_sort_value(name):
            return float(name.split('.')[1][:-1])

        df = df.sort_values(by=df.columns[0], key=lambda x: x.apply(get_sort_value), ascending=True).set_index(df.columns[0]).round(2)
        df.to_csv(f'~/out_stats_fastq/SAMEA110452918_out_stat/Taxa_stats_SAMEA110452918_tresh_{threshold}.csv')

    def run_analysis(self, thresholds):
        for threshold in thresholds:
            species_main = self.get_data(threshold)
            Taxa_stats, ground_truth = self.compute_jaccard_scores(species_main)
            self.compute_bray_curtis_dissimilarity(species_main, Taxa_stats, ground_truth, threshold)

