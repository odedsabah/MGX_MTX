#!/usr/bin/python3

# Upload packages
import sys
import gzip
import os
import pandas as pd

'''selected_reads(sample_size) is a function that returns a list of the number of reads to
select at different sequencing depths, based on an input sample_size'''

def selected_reads(sample_size):
    n_serial = (list(range(1, 9)) + list(range(10, 18, 2)) + list(range(20, 49, 5)) + list(range(50, 99, 10)) +
                list(range(100, 200, 100)) + list(range(1000, 10001, 1000)))
    n_serial = [i * 1e6 for i in n_serial]
    selected_read = [sample_size // i for i in [i for i in n_serial]]
    dict_selected_read = dict(zip(n_serial, selected_read))
    return dict_selected_read

def prepare_fastq_file(fastq_file, fastq_file_out, jump, num_reads):
    with gzip.open(fastq_file, "rt") as fin, gzip.open(fastq_file_out, "wt") as fout:
        counter = 0
        for line in fin:
            line += fin.readline()
            line += fin.readline()
            line += fin.readline()
            counter += 1
            if counter % jump == 0:
                fout.write(line)
                if counter // jump == num_reads:
                    break

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
    df.to_csv('Taxa_stats_SAMEA110452924_1.csv')

def main():

    if len(sys.argv) != 3:
        quit("\nUsage: " + sys.argv[0] + " <path_fastq_file> " + " <path_file_metaphlan_file \n\n")

    fastq_file = sys.argv[1]
    Path_MP4_files = sys.argv[2]

    sample_size = 258e6
    dict_selected_read = selected_reads(sample_size)

    if not os.path.isdir(f"mp4.depth_.{fastq_file.split('/')[5]}"):
        os.mkdir(f"mp4.depth_.{fastq_file.split('/')[5]}")
    id_file = f"mp4.depth_.{fastq_file.split('/')[5]}/" + fastq_file.split('/')[5]
    for i, (num_reads, jump) in enumerate(dict_selected_read.items()):
        fastq_file_out = f"{id_file}.{int(num_reads // 1e6)}M.fastq.gz"
        metaphlan_file_out = f"{id_file}.{int(num_reads // 1e6)}M.txt"
        prepare_fastq_file(fastq_file, fastq_file_out, jump, num_reads)
        os.system(f'/data1/software/metaphlan/run-metaphlan.sh {fastq_file_out} {metaphlan_file_out}'
                  f' 40 > {metaphlan_file_out}.stdout')
        os.system(f"rm -f {fastq_file_out}")

    species_main = get_data(Path_MP4_files)
    Taxa_stats, ground_truth = compute_jaccard_scores(species_main)
    compute_bray_curtis_dissimilarity(species_main, Taxa_stats, ground_truth)

if __name__ == '__main__':
    main()







