#!/usr/bin/python3

# Upload packages
import sys
import os
import pandas as pd

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

    cols = df.columns
    split_cols = [col.split("-") for col in cols]

    processed_cols = []  # keep track of processed columns

    # loop over all unique pairs of columns
    for i in range(len(split_cols)):
        if cols[i] in processed_cols:  # skip processed columns
            continue
        for j in range(i + 1, len(split_cols)):
            if (split_cols[i][1].split('.')[0] == split_cols[j][1].split('.')[0] and
                split_cols[i][0] != split_cols[j][0]):
                col, feat = cols[i], cols[j]
                species1 = df.loc[df[col] > 0, :].index
                species2 = df.loc[df[feat] > 0, :].index
                intersection = len(set(species1).intersection(set(species2)))
                union = len(set(species1).union(set(species2)))
                score = intersection / union if union != 0 else 0
                # Sort the column names so each pair always appears in the same order
                feature_versusf = ' VS '.join(sorted([col, feat]))
                # add the score to the similarity_scores dictionary
                similarity_scores[feature_versusf] = score
                processed_cols.append(cols[i])  # mark the column as processed
                processed_cols.append(cols[j])  # mark the column as processed
                break  # stop further analysis with the column

    # create new dataframe with the similarity scores
    Taxa_stats = pd.DataFrame(list(similarity_scores.items()), columns=['Cols_name', 'jaccard_scores']).set_index(
        'Cols_name')
    return Taxa_stats

def compute_bray_curtis_dissimilarity(df, Taxa_stats):
    def distance_calculation(u, v):
        l2 = ((u - v) ** 2).sum() ** 0.5
        l1 = sum(abs(u - v))
        den = sum(u + v)
        distance = l1 / den if den != 0 else 0  # Prevent zero division
        return distance, l1, l2

    dissimilarity_scores = {}
    l1_scores = {}
    l2_scores = {}

    # loop over all unique pairs of columns in Taxa_stats
    for col_vs_feat in Taxa_stats.index:
        col, feat = col_vs_feat.split(' VS ')
        u = df[col]
        v = df[feat]
        distance, l1, l2 = distance_calculation(u, v)

        # Add to dictionaries
        dissimilarity_scores[col_vs_feat] = distance
        l1_scores[col_vs_feat] = l1
        l2_scores[col_vs_feat] = l2

    dissimilarity_matrix = pd.DataFrame(
        {'Dissimilarity': dissimilarity_scores, 'l1_score': l1_scores, 'l2_score': l2_scores})

    # Merge the Taxa_stats and dissimilarity_matrix dataframes on the index
    df = pd.concat([Taxa_stats, dissimilarity_matrix], axis= 1)
    return df

def parse_sort_key(item):
    # split the item by ' VS ' and '-'
    parts = item.split(" VS ")
    # separate the first number and the number before "M" for each part
    keys = [(int(p.split('-')[0]), int(p.split('-')[1].split('M')[0])) for p in parts]
    # use the minimum value of the numbers before "M" and the minimum of the first numbers for sorting
    return min(k[1] for k in keys), min(k[0] for k in keys)

def sort_df(df):
    df.reset_index(inplace=True)
    # sort the column names using the defined key
    sorted_indices = sorted(df["index"], key=parse_sort_key)

    # reorder the DataFrame's rows
    df.set_index("index", inplace=True)
    df = df.reindex(sorted_indices)
    df = df.round(decimals=3)

    # print the DataFrame
    df.to_csv("~/test_split.csv")
    # print(df)
    return df

def main():

    if len(sys.argv) != 2:
        quit("\nUsage: " + sys.argv[0] + " <path_file_metaphlan_file> \n\n")

    Path_MP4_files = sys.argv[1]

    species_main = get_data(Path_MP4_files)
    Taxa_stats = compute_jaccard_scores(species_main)
    df = compute_bray_curtis_dissimilarity(species_main, Taxa_stats)
    sort_df(df)

if __name__ == '__main__':
    main()







