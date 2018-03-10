# Scripts used in "Skewed X-inactivation is common in the general female population"

**[heteroz-table-maker.sh](heteroz-table-maker.sh)** - this is the main script used for getting the table with paternal and maternal counts of each SNV in each female child, it incorporates the usage of all other scripts described below



**[nonexon_filter_RNA.py](nonexon_filter_RNA.py)** - this script is for getting a RNAseq counts file with exon snvs for current family child

example of running the script:

nonexon_filter_RNA.py -i {input_file} -bed {bed_file} -o {output_file_name}

Input:

- (-i) a file with RNAseq data for the child of a current family
- (-bed) a .bed file with exon annotation

Output:
- (-o) the name of the output file which will contain RNAseq data for SNVs which are located in exons



**[st3_heteroz_in_child_dnapart.py](st3_heteroz_in_child_dnapart.py)** - this is a script for getting heterozygotic snvs for current family (on dna basis) 

example of running the script:

st3_heteroz_in_child_dnapart.py -i {input_file.vcf} -o {output_file_name.txt}

Input:

- (-i) a VCF file summarizing genotype calls for particular family

Output:

- (-o) the name of the output file which will contain a list of positions of SNVs which are heterozygous in the child on dna basis



**[st3_heteroz_in_child_rnapart.py](st3_heteroz_in_child_rnapart.py)** - this is a script for getting heterozygotic snvs for current family (on rna basis)

example of running the script:

st3_heteroz_in_child_rnapart.py -i {input_file} -o {output_file_name.txt}

Input:

- (-i) a file with RNAseq data for the child of the current family

Output:

- (-o) the name of the output file which will contain a list of positions of SNVs which have heterozygous expression



**[select_by_loci_rnapart.sh](select_by_loci_rnapart.sh)** - this is a script for selecting RNAseq data for heterozygous SNVs from the original file

example of running the script:

./select_by_loci_rnapart.sh {list_of_heteroz_loci.txt} {input_original_file} {output_file}

Input:

- {list_of_heteroz_loci.txt}: a list of heterozygous SNVs
- {input_original_file}: a file with RNAseq data for the child of the current family

Output:
- {output_file}: the name of the output file which will contain RNAseq data for positions from the input list



**[merge_table_dna_rna_origin.py](merge_table_dna_rna_origin.py)** - this is a script for merging dna and rna information for one family in one table and for defining paternalCount and maternalCount for SNVs

example of running the script:

merge_table_dna_rna_origin.py -i_rna {input_rna_data} -i_dna {input_dna_data.vcf} -o {output_file_name.txt} -f {family_name}

Input:

- (-i_rna) a file with RNAseq data for heterozygous SNVs of the child of the current family
- (-i_dna) a .vcf file with genotype data for heterozygous SNVs of the child of the current family
- (-f) current family name 

Output:

- (-o) the name of the output file which will contain a merged table for the current family
