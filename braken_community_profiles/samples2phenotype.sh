#!/usr/bin/env bash

# This program receives MTX data without a phenotype
# setting classifies the files into folders by phenotypes in MGX files

# input - files MTX data without a phenotype
# output - files MTX Classified in folders by phenotypes


for f in $( ls /home/odeds/out_braken_esco/ | grep "bracken_output_kraken2_report_HumanRef_v1.0.1_" ); do
  pheno='undefined'
  if [[ -f /home/odeds/out_braken_esco/MGX_CD/"${f}" ]]; then
      pheno='CD'
  elif [[ -f /home/odeds/out_braken_esco/MGX_UC/"${f}" ]]; then
      pheno='UC'
  elif [[ -f /home/odeds/out_braken_esco/MGX_control/"${f}" ]]; then
      pheno='control'
fi
#  iden=$( echo "${f}" | cut -d "_" -f 7 | cut -d "." -f 1 )
#  pheno=$( grep "${iden}" /home/odeds/HMP_Metadata/hmp2_metadata.csv | cut -d "," -f 71 )
#  mv /home/odeds/out_braken_esco/MTX/"${f}" /home/odeds/out_braken_esco/MTX/MTX_"${pheno}"
#  echo -e "mv\t/home/odeds/out_braken_esco/${f}\t/home/odeds/out_braken_esco/MTX_${pheno}/"

mv "/home/odeds/out_braken_esco/${f}" "/home/odeds/out_braken_esco/MTX_${pheno}/"
  done

