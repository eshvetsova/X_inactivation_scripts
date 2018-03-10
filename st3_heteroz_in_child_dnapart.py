# this is a script for getting heterozygotic snvs for current family (on dna basis) 
## example of running the script:
## st3_heteroz_in_child_dnapart.py -i {input_file.vcf} -o {output_file_name.txt}
## Input:
##   - (-i) a VCF file summarizing genotype calls for particular family
## Output:
##   - (-o) the name of the output file which will contain a list of positions of SNVs which are heterozygous in the child on dna basis
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="input_file")
parser.add_argument("-o", type=str, help="output_file")
args = parser.parse_args()

output=open(args.o, "w")
input=args.i
output.write('CHROM' + '\t' +	'POS' + '\n')
import vcf
import vcf.filters
vcf_reader = vcf.Reader(open(input, 'r'))
for record in vcf_reader:
    #-1 in the case of family of 2 members
    if record.genotype(vcf_reader.samples[-1])['GT'] in ['0|1','1|0']:
        output.write(str(record.CHROM) + '\t' + str(record.POS) + '\n')
output.close()
    
