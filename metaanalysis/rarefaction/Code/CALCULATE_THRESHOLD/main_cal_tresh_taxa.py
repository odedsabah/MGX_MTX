
# 
# import argparse
# from pathlib import Path
# from Stat_from_select import MetaphlanAnalysis
# from Stat_from_split import MetaphlanAnalysis_from_split
# 
# # def main():
# #     parser = argparse.ArgumentParser(description='Process Metaphlan output files.')
# #     parser.add_argument('path_from_select', type=Path, help='Path to Metaphlan output files from select.')
# #     parser.add_argument('path_from_split', type=Path, help='Path to Metaphlan output files from split.')
# #     args = parser.parse_args()
# #
# #     analysis = MetaphlanAnalysis(path_mp4_files=args.path_from_select)
# #     analysis.run_analysis(thresholds=[0, 0.001, 0.01, 0.1, 1])
# #     analysis = MetaphlanAnalysis_from_split(path_mp4_files=args.path_from_split)
# #     analysis.run_analysis_from_split(thresholds=[0, 0.001, 0.01, 0.1, 1])
# #
# # if __name__ == '__main__':
# #     main()

#!/usr/bin/python3

import sys
from concurrent.futures import ProcessPoolExecutor
from fastq_selector import FastqProcessor
from fastq_splitter import FastqSplitter
from Stat_from_select import MetaphlanAnalysis
from Stat_from_split import MetaphlanAnalysis_from_split

def main():
    if len(sys.argv) != 3:
        print("\nUsage: " + sys.argv[0] + " <Path to the FASTQ file> <Path to the Read Stats file> \n\n")
        sys.exit(1)

    Path_to_the_FASTQ_file = sys.argv[1]
    Path_to_the_Read_Stats_file = sys.argv[2]

    with ProcessPoolExecutor() as executor:
        processor = FastqProcessor(fastq_file=Path_to_the_FASTQ_file, read_stats=Path_to_the_Read_Stats_file)
        splitter = FastqSplitter(fastq_path=Path_to_the_FASTQ_file, read_stats=Path_to_the_Read_Stats_file)

        processor_future = executor.submit(processor.process)
        splitter_future = executor.submit(splitter.split)

        # Wait for both processes to finish and get their results
        path_selector_out = processor_future.result()
        path_splitter_out = splitter_future.result()

        threshold = [0, 0.001, 0.01, 0.1, 1]
        analysis_future1 = executor.submit(MetaphlanAnalysis, path_mp4_files=path_selector_out)
        analysis_future2 = executor.submit(MetaphlanAnalysis_from_split, path_mp4_files=path_splitter_out)

        analysis1 = analysis_future1.result()
        analysis1.run_analysis(thresholds=threshold)

        analysis2 = analysis_future2.result()
        analysis2.run_analysis_from_split(thresholds=threshold)

if __name__ == '__main__':
    main()
