# program to convert DNA to the six possible protiens (* = stop)
import sys
from dpa_funcs import geneFASTA
from codon_tree import Codon_Tree

file = sys.argv[-1]
sequence = geneFASTA(sys.argv[-2])


tree = Codon_Tree(file)

REVERSE_COMP = lambda seq: seq[::-1].translate(seq.maketrans("ATGC", "TACG"))


all_protiens = [[] for _ in range(6)]

rf_offset = 0

for seq in [sequence, REVERSE_COMP(sequence)]:
    # for each reading frame
    for rf in range(3):
        proteins = []
        for i in range(rf, len(seq) - 2, 3):
            codon = seq[i:i+3]

            aa = tree.find_aa(codon)
            
            for i in range(len(proteins)):
                proteins[i] = proteins[i] + aa

            if (aa == "M"):
                proteins.append(aa)
            elif (aa == "*"):
                for protein in proteins:
                    all_protiens[rf + rf_offset].append(protein)
                proteins = []
    
    rf_offset = 3

for i in range(len(all_protiens)):
    print()
    if (i % 3 == 0): 
        print("Major Strang Reading Frame", i)
    else:
        print("Minor Strand Reading Frame", i % 3)

    for protein in all_protiens[i]:
        print(protein)