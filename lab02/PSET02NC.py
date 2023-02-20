# run with $python3 file.py file.fasta codon_to_aa.txt


# program to convert DNA to the six possible protiens (* = stop)
import sys
from dpa_funcs import geneFASTA # import prof aalberts geneFasta function
from codon_tree import Codon_Tree # import tree to be built

file = sys.argv[-1]
sequence = geneFASTA(sys.argv[-2])


# plain codon tree (unoptomized)
tree = Codon_Tree(file)

# make reverse comp
REVERSE_COMP = lambda seq: seq[::-1].translate(seq.maketrans("ATGC", "TACG"))

all_protiens = [[] for _ in range(6)]

rf_offset = 0

# go through each rf
for seq in [sequence, REVERSE_COMP(sequence)]:
    # for each reading frame
    for rf in range(3):
        proteins = []
        for i in range(rf, len(seq) - 2, 3):
            codon = seq[i:i+3]

            # find amino acid for codon
            aa = tree.find_aa(codon)
            
            # add that amino acid to open reading frames
            for i in range(len(proteins)):
                proteins[i] = proteins[i] + aa

            # if its a start start new protien
            if (aa == "M"):
                proteins.append(aa)

            # if stop end all protiens
            elif (aa == "*"):
                for protein in proteins:
                    all_protiens[rf + rf_offset].append(protein)
                proteins = []
    
    rf_offset = 3

# print stuff
for i in range(len(all_protiens)):
    print()
    if (i < 3): 
        print("Reading Frame", i)
    else:
        print("Reverse Reading Frame", i % 3)

    for protein in all_protiens[i]:
        print(protein)