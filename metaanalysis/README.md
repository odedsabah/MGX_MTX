# Oded's M.Sc. thesis

## Research question
Can we identify a consistent set of taxa that are associated with Crohn's disease/Ulcerative colitis compared to healthy humans?

We want to:
* Identify such list over multiple datasets
* If no such list exists - explain why
* Determine what is the most reliable methodology to find such list

## High-level plan
0. Do literature search about similar meta-analysis projects
1. Identify relevant datasets
2. Determine dataset metadata for each dataset
3. Read literature, understand how people generate such lists
4. Determine community composition for each sample
5. Determine whether the datasets are comparable
6. Decide bioinformatics/statistical procedure for determining list
7. Analyze the results

## Workplan
### 0. Do literature search about similar meta-analysis projects
We are interested in other meta-anlyses that were done on IBD or other diseases.
Create a table with answers to the following:
* What data was used? MGX, 16S?
* What methods were used? How was community profiling done, did the authors look at different taxonomic levels separately or all together, what statictical/ML methods were used to create the list?
* Did the authors made sure that the data is comparable (e.g. by comparing the control?)
* Did the authors analyze each dataset separately or all the datasets together? 
* Did the different datasets were considered based on their size relative to other datasets? Was the same number of samples taken from each dataset? 
* Did the authors took into account time-series datases?
* Were metadata (age, sex, nationality, calprotectin) taken into account?

### 1. Identify relevant datasets
Create a table with all the datasets we will work on. Consider the following datasets:
MGX Available on vega:
* ibdmdb [paper](https://www.nature.com/articles/s41586-019-1237-9). CD: ```/data1/Human/ibdmdb/CD/```, UC: ```/data1/Human/ibdmdb/UC/```, control: ```/data1/Human/ibdmdb/control/```
* ibdmdb pilot. 
* metahit
* metahit2
* Lewis
* HMP1
* HMP2
* HMP3
* Gevers (PRJNA237362): [paper](https://www.sciencedirect.com/science/article/pii/S1931312814000638)
* Eran Elinav's paper (only part of the data is available on vega) [paper](https://pubmed.ncbi.nlm.nih.gov/35931020/)
* EGAD00001001991
Also look for other data.

For each project, the raw data for the samples is located under the raw.d directory, e.g. ```/data2/Human/HMP.phase1/Stool/raw.d```. Sample statistics file is named <something>.read-stats.txt under raw.d. For example: ```/data2/Human/HMP.phase1/Stool/raw.d/Stool.read-stats.txt```. Open an issue is this file does not exist.

To find the number of samples and the average sequencing depth:
```
tail -n +3 /data2/Human/HMP.phase1/Stool/raw.d/Stool.read-stats.txt | awk '{n++; bp+=($5+$8)} END{print n"\t"(bp/(n*1000000000))}'
```
  
  Required information:
* In the table:
  * Project name
  * Project NCBI/other ID if available
  * Project paper
  * Number of control samples
  * Number of CD samples
  * Number of UC samples
  * Is time series?
  * Average sequencing depth (number of bps)
  * Sequencing technology (Illumina)
  * Read size (150bp...)
* For each sample, we would like to get the following metadata:

To get the read size, pick a random fastq file for one of the samples and run
```
gunzip -c mysample.1.fastq.gz | awk '{if(NR%4==2) {print length($0)}}' | head
```

For each project download the metadata file.

### 2. High-level view of the meta-analysis process
These are the steps that we plan to take:
1. Evaluate community composition for the samples
2. Evaluate the comparability between the datasets
3. Naive approach 1: find separating taxa between the group of healthy and controls in each dataset
4. Naive approach 2: look for differences in community composition between healthy and CD/UC (beta-diversity)
5. Less naive: consider other parameters (age, sex, health status)
6. Conclusions?
7. Guidelines regarding performing an experiment
   * What is the minimal number of participants required for a dataset to discover differentiating taxa?
   * What is the minimal abundance for taxa that should be considered?
   * At what taxonomic level(s) can we see differences?
 
### 3. Low-level view of the meta-analysis process
#### 1. Evaluate community composition for the samples

*How to choose an algorithm?*

We will choose metaphlan4 because it is the most popular algorithm with the most updated database of all. Kraken2 and Centrifuge provide a lot of false positives and mOTUs2 does not have sufficiently large reference database.

*How to do rarefaction?*
We need to identify, for each threshold (e.g. 1%, 0.1%, 0.01%), what is the number of reads that is required to get "everything".
How we will do it:
1. Identify very large samples (Eran Elinav's dataset have some)
2. Run metaphlan4 on the entire dataset (done)
3. for each n in (1M, 2M, 3M, 4M, 5M, 6M, 8M, 10M, 12M, 14M, 16M, 18M, 20M, 25M, 30M, 35M, 40M, 45M, 50M, 60M, 70M, ...): 
   * Create a dataset of the required size by selecting every (sample size)//n read
   * Run metaphlan4 on the sample
   * delete the sample
4. For each threshold (1, 0.1, 0.01):
   * Calculate Jaccard index of species above the threshold and the entire sample. Create a graph that shows that
   * Calculate the difference in relative abundance between each sub-sample and the complete sample
   
For development, use this sample (5,243,596 reads):
```
/data2/Human/PRJEB50555/raw.d/SAMEA110452936/9841_R1.fastq.gz
```

For actual analysis, use this sample (299,380,873 reads)
```
/data2/Human/PRJEB50555/raw.d/SAMEA110452975/9836_R1.fastq.gz 
```

Running metaphlan4:
```
conda activate base
/home/itaish/software/processing/run-metaphlan4.sh
```

