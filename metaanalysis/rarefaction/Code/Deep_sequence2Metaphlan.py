#!/usr/bin/python3

# Upload packages
import sys
import os
import pandas as pd

'''
The script expects one command-line argument as input:

1. `path_file_metaphlan_file`: The path to the directory containing Metaphlan output files.

When executing the script from the command line, you would provide this argument. Here's an example:

<python Deep_sequence2Metaphlan.py /path/to/metaphlan_output_directory>

As for the output, the script generates a CSV file named "Taxa_stats_{id_file}_tresh_{Threshold}.csv".
 The file contains the results of the data analysis, including Jaccard similarity scores and Bray-Curtis dissimilarity scores.

The CSV file includes the following columns:
- `Col_name`: The column names representing the samples.
- `Num_of_species`: The number of species in each sample.
- `Ground_truth`: The name of the ground truth sample with the highest numerical value in the column names.
- `Dissimilarity`: The Bray-Curtis dissimilarity scores between each sample and the ground truth sample.
- `l1_score`: The L1 scores (sum of absolute differences) between each sample and the ground truth sample.
- `l2_score`: The L2 scores (Euclidean distances) between each sample and the ground truth sample.

** all the ration on between "ground_truth" this is a file with a large max of 

The output CSV file is saved in the same directory as the script.

Please note that the script assumes the presence of Metaphlan output files in the specified directory
,and it expects the files to be in a specific format. 
Ensure that the directory contains the necessary files for the script to execute successfully.
'''

def get_data(Path_MP4_files,Threshold=1):
    species_main = None
    samples = [x for x in os.listdir(Path_MP4_files) if x.endswith(".txt")]
    for sample in samples:
        species_abundance = dict()
        sample_name = sample[:-4]
        with open(f'{Path_MP4_files}/{sample_name}.txt') as s:
            f = s.readlines()
            for line in f:
                # k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Lachnospiraceae|g__Coprococcus|s__Coprococcus_comes 2|1239|186801|186802|186803|33042|410072        0.00264
                if line.startswith("k__Bacteria"):
                    try:
                        species = line.strip().split("\t")[0].split("|")[-1]
                        abundance = float(line.split()[2])
                        if species.startswith('s__') and abundance >= Threshold:
                            species_abundance[species] = abundance
                    except:
                        print(f'this value: {line.split()[2]} is not an abundance')
        Taxa_Abundance = pd.DataFrame((species_abundance.items()), columns=['Species',sample_name]).set_index('Species')
        species_main = pd.concat([species_main,Taxa_Abundance], axis=1, join="outer").fillna(0)
    return species_main

def compute_jaccard_scores(df):
    # initialize an empty dictionary to hold the similarity scores
    similarity_scores = {}
    ground_truth = max(df.columns, key=lambda x: int(''.join([i for i in x.split('.')[-1] if i.isdigit()])))
    # loop over all pairs of columns
    for col in df.columns:
        # compute the Jaccard score between the two columns
        species1 = df.loc[df[col] > 0, :].index
        species2 = df.loc[df[ground_truth] > 0, :].index
        intersection = len(set(species1).intersection(set(species2)))
        union = len(set(species1).union(set(species2)))
        score = intersection / union
        # add the score to the similarity_scores dictionary
        similarity_scores[col] = score
    # create new columns in the dataframe with the similarity scores
    Taxa_stats = pd.DataFrame([(col, sum(df[col] > 0 ), similarity_scores[col]) for col in df.columns],
                              columns=['Col_name', 'Num_of_species', 'Ground_truth']).set_index('Col_name')
    return Taxa_stats, ground_truth

def compute_bray_curtis_dissimilarity(df,Taxa_stats, ground_truth):
    '''Computes the Bray-Curtis dissimilarity between all columns in df and a specific column.'''
    def distance_calculation(u, v):
        l2 = ((u - v) ** 2).sum() ** 0.5
        l1 = sum(abs(u - v))
        den = sum(u + v)
        distance = l1 / den
        return distance, l1, l2

    # get the column to compare to
    u = df[ground_truth]
    # initialize an empty list to hold the dissimilarity scores
    dissimilarity_scores = []
    l1_scores = []
    l2_scores = []
    # loop over all columns
    for col in df.columns:
        # compute the Bray-Curtis dissimilarity between the two columns
        v = df[col]
        distance, l1, l2 = distance_calculation(u, v)
        # add the distance score to the list of dissimilarity scores
        dissimilarity_scores.append(distance)
        l1_scores.append(l1)
        l2_scores.append(l2)
    # create a DataFrame with the dissimilarity scores and return it
    dissimilarity_matrix = pd.DataFrame({'Dissimilarity': dissimilarity_scores, 'l1_score': l1_scores, 'l2_score': l2_scores},
                                        index=df.columns)
    df = pd.concat([Taxa_stats, dissimilarity_matrix], axis=1).reset_index()

    def get_sort_value(name):
        return float(name.split('.')[1][:-1])

    df = df.sort_values(by=df.columns[0], key=lambda x: x.apply(get_sort_value), ascending=True).set_index(df.columns[0]).round(2)
    df.to_csv('Taxa_stats_SAMEA110452924_test.csv')

def main():

    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <path_file_metaphlan_file \n\n")

    Path_MP4_files = sys.argv[1]

    species_main = get_data(Path_MP4_files)
    Taxa_stats, ground_truth = compute_jaccard_scores(species_main)
    compute_bray_curtis_dissimilarity(species_main, Taxa_stats, ground_truth)

if __name__ == '__main__':
    main()







