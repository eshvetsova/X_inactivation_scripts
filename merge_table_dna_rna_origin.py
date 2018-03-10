# this is a script for merging dna and rna information for one family in one table and for defining paternalCount and maternalCount for SNVs
## example of running the script:
## merge_table_dna_rna_origin.py -i_rna {input_rna_data} -i_dna {input_dna_data.vcf} -o {output_file_name.txt} -f {family_name}
## Input:
##   - (-i_rna) a file with RNAseq data for heterozygous SNVs of the child of the current family
##   - (-i_dna) a .vcf file with genotype data for heterozygous SNVs of the child of the current family
##   - (-f) current family name 
## Output:
##   - (-o) the name of the output file which will contain a merged table for the current family
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i_rna", type=str, help="input_file_rna_part")
parser.add_argument("-o", type=str, help="output_file")
parser.add_argument("-i_dna", type=str, help="input_file_dna_part")
parser.add_argument("-f", type=str, help="family")
args = parser.parse_args()

output = open(args.o, "w")
output.write('family\tchr\tpos\tfatherGt\tmotherGt\tchildGt\tchildRefCount\tchildAltCount\tchildFromFatherCount\tchildFromMotherCount\n')
import vcf
import vcf.filters
rna_input = open(args.i_rna, "r")
vcf_reader = vcf.Reader(open(args.i_dna, 'r'))
records={}
samples=[]
rna_snps=[]
for cur_s_name in vcf_reader.samples:
        samples.append(cur_s_name)
for record in vcf_reader:
    cur_genotypes=[]
    for i in samples:
        cur_genotypes.append(record.genotype(i)['GT'])
    records[int(record.POS)]=cur_genotypes
for line in rna_input:
    if line.startswith('X'):
        line=line.strip().split()
        rna_snps.append(int(line[1]))
        if (int(line[1]) in records.keys()):
            f=records[int(line[1])][0]
            if len(records[int(line[1])]) == 3:
		m=records[int(line[1])][1]
            	c=records[int(line[1])][2]
	    else:
		m="NA"
		c=records[int(line[1])][1]
            if ((f in ["0|0", "1|1"]) or (m in ["0|0", "1|1", "NA"])) and (c in ["0|1", "1|0"]):
                if f == m:
                    fcount="NA"
                    mcount="NA"
                elif (f == "0|0") or (m == "1|1"):
                    fcount=line[5]
                    mcount=line[6]
                else:
                    fcount=line[6]
                    mcount=line[5]
                output.write(args.f + '\tX\t' + line[1] + '\t' + f +'\t' + m  + '\t' + c + '\t' + line[5] + '\t' + line[6] + '\t' + fcount + '\t' + mcount + '\n')
            else:
                output.write(args.f + '\tX\t' + line[1] + '\t' + f +'\t' + m + '\t' + c + '\t' + line[5] + '\t' + line[6] + '\t' + "NA" + '\t' + "NA" + '\n')
        else:
            output.write(args.f + '\tX\t' + line[1] + '\t' + "NA" +'\t' + "NA" + '\t' + "NA" + '\t' + line[5] + '\t' + line[6] + '\t' + "NA" + '\t' + "NA" + '\n')

#for i in records.keys():
#    if not (i in rna_snps):
#        output.write(args.f + '\tX\t' + str(i) + '\t' + records[i][0] +'\t' + records[i][1] + '\t' + records[i][2] + '\t' + "NA" + '\t' + "NA" + '\t' + "NA" + '\t' + "NA" + '\n')

rna_input.close()
output.close()
