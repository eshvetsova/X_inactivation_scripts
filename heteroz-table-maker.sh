#!/bin/bash
counts_dir='./arcout'
dna_vcf_file='chrX_nonPAR_part.phased.abc.vcf.gz'
bed_annot='meta-exons_v71_cut_sorted_22-05-14.bed'
working_dir='./heteroz_table_files/'
mkdir $working_dir

mapping_table_for_children='mapping_table_children_example.txt'

cd $working_dir
#getting all exon snvs from vcf file using bed annotation file
echo "getting all exon snvs from vcf file using bed annotation file..."
vcftools --gzvcf ../$dna_vcf_file --out output_exon_DNA --bed ../$bed_annot --recode

#for each family
echo '' > families_check.txt
for file in `find ../$counts_dir -type f -name "*.merged.rorg.chrX.txt"`; do
	fname="${file##*/}"
	name="${fname%%.*}"
	echo ${name}
	family_name_x=`grep -P "${name}\t" ../${mapping_table_for_children} | awk '{print $2}'`
	echo ${family_name_x}
	family_name="${family_name_x%?}"
	echo ${family_name}
	#getting a file-list with family members ids:
	echo ${family_name}a > ${family_name}-family
	echo ${family_name}b >> ${family_name}-family
	echo ${family_name}c >> ${family_name}-family
	
	#DNA PART	
	#getting a vcf file with members of current family:
	echo "1. getting a vcf file with members of ${family_name}..."
	vcftools --vcf output_exon_DNA.recode.vcf --out ${family_name}-family --keep ${family_name}-family --recode
	
	#getting heterozygotic snvs for current family (on dna basis) 
	#heteroz_in_child_${family_name}_dna.txt - (chr)(pos) list of heteroz snvs
	echo "2. getting heterozygotic snvs for ${family_name} (on dna basis)..."
	python2.7 ../st3_heteroz_in_child_dnapart.py -i ${family_name}-family.recode.vcf -o heteroz_in_child_${family_name}_dna.txt
	
	#RNA PART
	#getting a RNAseq counts file with exon snvs for current family child
	echo "3. getting a RNAseq counts file with exon snvs for ${family_name} child..."
	python2.7 ../nonexon_filter_RNA.py -i ../${counts_dir}/${fname} -bed ../$bed_annot -o output_exon_RNA_${family_name}c.txt
	
	#getting heterozygotic snvs for current family (on rna basis)
	echo "4. getting heterozygotic snvs for ${family_name} (on rna basis)..."
	python2.7 ../st3_heteroz_in_child_rnapart.py -i output_exon_RNA_${family_name}c.txt -o heteroz_in_child_${family_name}_rna.txt
	
	#getting a merged list-file of heterozygotic snvs (on dna and rna basis)
	#heteroz_all_${family_name}.txt - list of all heterozygotic snvs for current family
	echo "5. getting a merged list-file of heterozygotic snvs (on dna and rna basis)..."
	cat heteroz_in_child_${family_name}_dna.txt heteroz_in_child_${family_name}_rna.txt | sort | uniq > heteroz_all_${family_name}.txt

	#selecting heterozygotic snvs from original files
	echo "6. selecting heterozygotic snvs from original files..."
	#DNA information
	vcftools --vcf ${family_name}-family.recode.vcf --out heteroz_all_${family_name}_dna --positions heteroz_all_${family_name}.txt --recode
	#RNA information	
	../select_by_loci_rnapart.sh heteroz_all_${family_name}.txt output_exon_RNA_${family_name}c.txt heteroz_all_${family_name}_rna.txt
	
	#merging dna and rna information in one table
	
	echo "7. merging dna and rna information in one table..."
	echo ${family_name}
	python2.7 ../merge_table_dna_rna_origin.py -i_rna heteroz_all_${family_name}_rna.txt -i_dna heteroz_all_${family_name}_dna.recode.vcf -o merge_table_${family_name}.txt -f ${family_name}
done
cat merge_table*.txt | sort | uniq > final_table_for_all_families.txt
