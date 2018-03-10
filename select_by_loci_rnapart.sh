#!/bin/bash
# this is a script for selecting RNAseq data for heterozygous SNVs from the original file
## example of running the script:
## ./select_by_loci_rnapart.sh {list_of_heteroz_loci.txt} {input_original_file} {output_file}
## Input:
##   - {list_of_heteroz_loci.txt}: a list of heterozygous SNVs
##   - {input_original_file}: a file with RNAseq data for the child of the current family
## Output:
##   - {output_file}: the name of the output file which will contain RNAseq data for positions from the input list
args=("$@")
loci=${args[0]}
all_snps=${args[1]}
loci_list=`cat $loci | awk '{print $2}'`

echo '' > ${args[2]} 
for cur_loci in $loci_list; do 
	grep "$cur_loci" $all_snps >> ${args[2]}
done
