##### PHYS 315: PS03 #####
#to call: python3 PS03s.py
#reads GenBank file (ecoNC_000912.2.gb)
#builds 'K12orfs.csv' with {geneName,-1,geneType,left,right,cds}
#and reports on number of genes at each location
#and prints tRNA and rRNA 

import sys   #system commands (for taking input from command line)
import string # for maketrans 

def geneFASTA(fastafile):
    fasta_seq = [ ]
    with open(fastafile, "r") as fin:
        for line in fin:
            if line[0] != ">":    #fasta header lines start with '>'
                fasta_seq.append(line.strip())
    gene = ''.join(fasta_seq )
    return gene

def revcomp(seq):
    complement = seq.maketrans("acgtuACGTU","tgcaaTGCAA")
    rc = seq.translate(complement)[::-1]
    return rc

genome = geneFASTA('ecoNC_000913.2.fasta')
reversecomp = revcomp(genome)

fout = open('K12orfs.csv','w')
fout2 = open("RNAfeatures.csv", 'w')
totalcoverage = 0

geneTypeD = {type : 0 for type in ['CDS','tRNA','rRNA','ncRNA']}

with open('./ecoNC_000913.2.gb') as fin:
    for line in fin:
        if line[:21].strip() in ['CDS','tRNA','rRNA','ncRNA']:  
            geneType = line[:21].strip()  #coding sequence, etc
            geneTypeD[geneType] += 1
            
            line2 = next(fin)       # get gene name
            while 'gene' not in line2:  
                line2 = next(fin)
            geneName = line2.split('gene="')[1][:-2]
            
            if 'join' in line[21:]: #gene contains a programmed frame shift
                pass                #ignore such for now???
            elif 'comp' in line[21:]:  #reversed gene, minus strand
                left, right= line[32:].split('..')
                left = int(left)
                right = int(right[:-2]) #[:-2] eliminates ')\n'
                cds = reversecomp[left:right] #NOT TRUE. FIX 
                totalcoverage += right - left
                fout.write("{},{},{},{},{},{}\n".format(geneName,-1,geneType,left,right,cds))
                if (geneType in ["tRNA", "rRNA"]):
                    fout2.write("{},{},{},{},{},{}\n".format(geneName,-1,geneType,left,right,cds))
            else:     #plus strand gene
                left, right= line[21:].split('..')
                left = int(left)
                right = int(right)
                totalcoverage += right - left
                cds = genome[left:right] #NOT TRUE. FIX.
                fout.write("{},{},{},{},{},{}\n".format(geneName,+1,geneType,left,right,cds))
                if (geneType in ["tRNA", "rRNA"]):
                    fout2.write("{},{},{},{},{},{}\n".format(geneName,+1,geneType,left,right,cds))


print(totalcoverage / len(genome))