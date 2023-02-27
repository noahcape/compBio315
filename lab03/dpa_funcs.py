#to call python3 Lab01-dpa.py [input.fasta]
import sys # command line tools

def geneFASTA(fastafile):
    fasta_seq = [ ]
    with open(fastafile, "r") as fin:
        for line in fin:
            if line[0] != ">":    #fasta header lines start with '>'
                fasta_seq.append(line.strip())
    gene = ''.join(fasta_seq )
    return gene

# gene = geneFASTA(sys.argv[-1])  #-1 is last command line argument
# print(gene[:1000])  # prints first part of genome

# table = gene.maketrans("ACGT","0123") 
# mRNA = gene.translate(table)

# print(mRNA[:1000])
# print(table)

