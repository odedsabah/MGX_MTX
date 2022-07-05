#!/usr/bin/python3


import pandas as pd
import argparse


def main():
    args = args_setup()
    # load Bracken species-level taxa output
    bracken_output = pd.read_csv(args.input_bracken, sep="\t")
    # load <exclusive_clusters.esco.gtdbtk> with tax_ids according to HumanRef v1.0.1
    esco_taxid = pd.read_csv(args.input_esco, sep="\t")
    # add the GTDB_taxonomy column by matching tax_id
    bracken_output = bracken_output.merge(esco_taxid[['tax_id', 'GTDB_taxonomy']], left_on='taxonomy_id', right_on='tax_id', how='inner')
    bracken_output.drop(['tax_id'], axis=1, inplace=True)
    # change the order of the columns:
    bracken_output = bracken_output[['GTDB_taxonomy', 'name', 'taxonomy_id', 'taxonomy_lvl', 'kraken_assigned_reads',
                                     'added_reads', 'new_est_reads', 'fraction_total_reads']]
    bracken_output.rename(columns={"name": "species_name"}, inplace=True)
    bracken_output.to_csv(args.output, index=False, header=True, sep="\t")
def args_setup():
    '''Command line arguments parsing function'''
    parser = argparse.ArgumentParser(description="script for adding full taxonomy information based on ESCO/GTDB taxonomy to Bracken report")
    parser.add_argument("input_bracken", help="path to Bracken output report file")
    parser.add_argument("input_esco", help="path to <taxids_exclusive_clusters.esco.gtdbtk> file with ESCO exclusive clusters")
    parser.add_argument("output", help="path to output file to save the modified Bracken report")
    return parser.parse_args()
if __name__ == "__main__":
    main()
