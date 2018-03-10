# this script is for getting a file with exon snvs for current family child
## example of running the script:
## nonexon_filter_RNA.py -i {input_file} -bed {bed_file} -o {output_file_name}
## Input:
##   - (-i) a file with RNAseq data for the child of a current family
##   - (-bed) a .bed file with exon annotation
## Output:
##   - (-o) the name of the output file which will contain RNAseq data for SNVs which are located in exons
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="input_file")
parser.add_argument("-o", type=str, help="output_file")
parser.add_argument("-bed", type=str, help="bed_file")
args = parser.parse_args()

genometype = open(args.i, 'r')
annotation = open(args.bed, "r")
output_exon = open(args.o, "w")

list_location =[]
dict_exon={}
dict_intron={}
coord_exon={}
coord_intron={}
current_geneID=""
dict_snp_ID={}


for line in genometype:
    if line.startswith("X"):
        line = line.strip().split('\t')
        location = int(line[1])
        list_location.append(location)


for line in annotation:
    if line.startswith("X"):
        line2=line
        line = line.strip().split('\t')
        start_exon=int(line[1]) 
        geneID=line[3].split('"')[1]
        if current_geneID == geneID:
            start_intron=end_exon+1
            end_intron=start_exon-1
            dict_intron[start_intron]=[geneID, ""]
            coord_intron[start_intron]=end_intron
        current_geneID=geneID
        end_exon=int(line[2])
        exonID=line[4].split("exon_id")[2].split('"')[1]
        dict_exon[start_exon]=[geneID, exonID]
        coord_exon[start_exon]=end_exon

start_coord_exon = coord_exon.keys()
start_coord_intron = coord_intron.keys()

def binary_search(a, x, start=0, end=None):
    if x < a[0]:
        return 0
    if end is None:
        end = len(a)
    while start < end:
        if start+1 == end:
           return a[start]
        mid = (start+end)//2
        midval = a[mid]
        if midval < x:
            start = mid
        elif midval > x: 
            end = mid
        else:
            return a[mid]
    return a[start]

start_coord_exon.sort()
start_coord_intron.sort()


for x in list_location:
    coord1=binary_search(start_coord_exon, x)
    if coord1 == 0:
        dict_snp_ID[x]=["", ""]
    else:
        coord2=coord_exon[coord1]
        if x < coord2:
            dict_snp_ID[x]=dict_exon[coord1]
        else:
            coord1=binary_search(start_coord_intron, x)
            if coord1 == 0:
                dict_snp_ID[x]=["", ""]
            else:
                coord2=coord_intron[coord1]
                if x < coord2:
                    dict_snp_ID[x]=dict_intron[coord1]
                else:
                    dict_snp_ID[x]=["", ""]


genometype.close()
genometype = open(args.i, "r")

IDs_dict=sorted(dict_snp_ID.items())
IDs=[]
for i in IDs_dict:
    IDs.append(i[1])

i=0
for line in genometype:
    if not line.startswith("X"):
        output_exon.write(line)
    else:
        line=line.strip()
        if IDs[i][1] != "":
            output_exon.write(line + "\n")
        i=i+1

output_exon.close()
annotation.close()
genometype.close()
        
         
