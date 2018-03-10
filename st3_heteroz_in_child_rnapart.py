# this is a script for getting heterozygotic snvs for current family (on rna basis)
## example of running the script:
## st3_heteroz_in_child_rnapart.py -i {input_file} -o {output_file_name.txt}
## Input:
##   - (-i) a file with RNAseq data for the child of the current family
## Output:
##   - (-o) the name of the output file which will contain a list of positions of SNVs which have heterozygous expression
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="input_file")
parser.add_argument("-o", type=str, help="output_file")
args = parser.parse_args()

output = open(args.o, "w")
output.write('CHROM' + '\t' +	'POS' + '\n')
input_f=open(args.i, "r")
for line in input_f:
    if line.startswith("X"):
        line=line.strip().split()
        position=line[1]      
        ref_count=int(line[5])
        alt_count=int(line[6])
        total_count=int(line[7])
        if (ref_count >= float(total_count)/4) and (alt_count >= float(total_count)/4):
            output.write('X' + '\t' + str(position) + '\n')
input_f.close()
output.close()
