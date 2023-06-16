#!/usr/bin/python3

import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd
import sys
import os


def xml_elements(root):
    elements_dict = {
        'PRIMARY_ID': None,
        'SECONDARY_ID': None,
        'STUDY_TITLE': None,
        'STUDY_ABSTRACT': None,
        'CENTER_PROJECT_NAME': None,
        'ENA-FASTQ-FILES': None,
        'ENA-RUN': None,
        'ENA-SUBMISSION': None,
        'ENA-SAMPLE': None,
        'ENA-EXPERIMENT': None,
        'ENA-SUBMITTED-FILES': None,
        'ENA-LAST-UPDATE': None,
        'ENA-SPOT-COUNT': None,
        'ENA-BASE-COUNT': None,
        'ENA-FIRST-PUBLIC': None
    }

    for study in root.findall('STUDY'):
        identifiers = study.find('IDENTIFIERS')
        elements_dict['PRIMARY_ID'] = identifiers.find('PRIMARY_ID').text if identifiers.find('PRIMARY_ID') is not None else 'NA'
        elements_dict['SECONDARY_ID'] = identifiers.find('SECONDARY_ID').text if identifiers.find('SECONDARY_ID') is not None else 'NA'

        descriptor = study.find('DESCRIPTOR')
        elements_dict['STUDY_TITLE'] = descriptor.find('STUDY_TITLE').text if descriptor.find('STUDY_TITLE') is not None else 'NA'
        elements_dict['STUDY_ABSTRACT'] = descriptor.find('STUDY_ABSTRACT').text if descriptor.find('STUDY_ABSTRACT') is not None else 'NA'
        elements_dict['CENTER_PROJECT_NAME'] = descriptor.find('CENTER_PROJECT_NAME').text if descriptor.find('CENTER_PROJECT_NAME') is not None else 'NA'

        study_links = study.find('STUDY_LINKS')
        if study_links is not None:
            for link in study_links.findall('STUDY_LINK'):
                xref_link = link.find('XREF_LINK')
                if xref_link is not None:
                    db = xref_link.find('DB').text
                    if db == 'ENA-FASTQ-FILES':
                        elements_dict['ENA-FASTQ-FILES'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'
                    elif db == 'ENA-RUN':
                        elements_dict['ENA-RUN'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'
                    elif db == 'ENA-SUBMISSION':
                        elements_dict['ENA-SUBMISSION'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'
                    elif db == 'ENA-SAMPLE':
                        elements_dict['ENA-SAMPLE'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'
                    elif db == 'ENA-EXPERIMENT':
                        elements_dict['ENA-EXPERIMENT'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'
                    elif db == 'ENA-SUBMITTED-FILES':
                        elements_dict['ENA-SUBMITTED-FILES'] = xref_link.find('ID').text if xref_link.find('ID') is not None else 'NA'

        study_attributes = study.find('STUDY_ATTRIBUTES')
        if study_attributes is not None:
            for attr in study_attributes.findall('STUDY_ATTRIBUTE'):
                tag = attr.find('TAG').text
                if tag == 'ENA-LAST-UPDATE':
                    elements_dict['ENA-LAST-UPDATE'] = attr.find('VALUE').text if attr.find('VALUE') is not None else 'NA'
                elif tag == 'ENA-SPOT-COUNT':
                    elements_dict['ENA-SPOT-COUNT'] = attr.find('VALUE').text if attr.find('VALUE') is not None else 'NA'
                elif tag == 'ENA-BASE-COUNT':
                    elements_dict['ENA-BASE-COUNT'] = attr.find('VALUE').text if attr.find('VALUE') is not None else 'NA'
                elif tag == 'ENA-FIRST-PUBLIC':
                    elements_dict['ENA-FIRST-PUBLIC'] = attr.find('VALUE').text if attr.find('VALUE') is not None else 'NA'

    return elements_dict

def main():
    if len(sys.argv) < 3:
        quit("\nUsage: " + sys.argv[0] + " <Path_XML_file> <Path_out> keyword1, keyword2, ...\n\n")

    Path_XML_file = sys.argv[1]
    Path_out = sys.argv[2]
    input_keywords = " ".join(sys.argv[3:])

    # Check if the input keywords are separated by commas
    if ',' not in input_keywords:
        quit("\nError: Keywords must be separated by commas. Example: keyword1, keyword2, keyword3\n\n")

    keywords = [word.strip() for word in input_keywords.split(",")]

    samples = [x for x in os.listdir(Path_XML_file) if not x.endswith(".txt")]

    df_list = []
    for id_project in samples:
        try:
            tree = ET.parse(os.path.join(Path_XML_file, id_project))
            root = tree.getroot()
            elements_dict = xml_elements(root)
            df_list.append(pd.DataFrame(elements_dict, index=[id_project]))
        except ET.ParseError:
            print(f"Skipped file: {id_project} - Invalid or not well-formed XML.")

    if df_list:
        df = pd.concat(df_list)

        # Filter rows based on any keyword in any column
        mask = df.apply(
            lambda row: any([keyword.lower() in val.lower() for val in row.astype(str) for keyword in keywords]),
            axis=1)
        df = df[mask]
        print(df)

        filename_keywords = "-".join(
            [keyword.upper() if len(keyword) <= 3 else keyword.title() for keyword in keywords])

        df.to_csv(f'{Path_out}xml_stats_{filename_keywords}.csv')

if __name__ == '__main__':
    main()

