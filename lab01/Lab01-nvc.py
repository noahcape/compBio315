import matplotlib.pyplot as plt
from dpa_funcs import geneFASTA
import sys

START = "TAC"
STOP_1 = "ATT"
STOP_2 = "ATC"
STOP_3 = "ACT"


# take string gene and return reverse complement
def rev_comp(gene):
    # reverse the gene
    gene = gene[::-1]

    # create mapping of complements
    table = gene.maketrans("ATCG", "TAGC")

    # return the proper mapping
    return gene.translate(table)

# create a dictionary with the distinct permutations of bases of certain length
def permute_bases_recursive(bases, length, index, key, dict):
    if (len(key) == length):
        dict[key] = 0

    if (index < len(bases)):
        # either include the base at certain index
        include = key + bases[index]

        # or exlcude it from final key
        exclude = key

        # for each iteration increment index
        index += 1

        # make recursive call on include and exclude
        permute_bases_recursive(bases, length, index, include, dict)
        permute_bases_recursive(bases, length, index, exclude, dict)

# function to call recursive function to permute bases
def generate_dict(bases, length):
    bases_dict = {}
    # call recursive method with initial values
    permute_bases_recursive(bases * length, length, 0, "", bases_dict)
    
    return bases_dict

# read gene and keep track of base freq in dictionary
def nucleotide_freq():
    gene = geneFASTA(sys.argv[-1])
    
    # generate empty dictionary
    freq_dict = generate_dict("ATGC", 1)

    # read base by base of gene
    for i in range(len(gene)):
        base = gene[i]
        # keep track of frequency
        freq_dict[base] += 1

    print(freq_dict)
    return freq_dict

# read gene and keep track of dinucleotide freq in dictionary
def dinucleotide_freq():
    gene = geneFASTA(sys.argv[-1])
    
    # generate empty dict for dinucleotide
    freq_dict = generate_dict("ATGC", 2)

    # read through gene
    for i in range(len(gene) - 1):
        base = gene[i:i+2]
        freq_dict[base] += 1

    print(freq_dict)
    return freq_dict

# note that is genome is linear and genome size is n, num dinucleotides is n-1
def analyze_nucleotide_dinucleotide_data(nucleotide_freqs, dinucleotide_freqs, genome_size):
    # determine which dinucleotide most differs from chance they appear together per genomes base frequency
    dinucleotide_ratio_deviation = generate_dict("ATGC", 2)

    # number_dinucleotides = sum(map(lambda x: dinucleotide_freqs[x], dinucleotide_freqs))

    # probs_b1_and_b2 = []
    # probs_dinucleotide = []
    # labels = []

    for key in dinucleotide_ratio_deviation:
        base_1 = key[0]
        base_2 = key[1]

        prob_base_1 = nucleotide_freqs[base_1] / genome_size
        prob_base_2 = nucleotide_freqs[base_2] / genome_size
        prob_dinucleotide = dinucleotide_freqs[key] / genome_size

        # probs_b1_and_b2.append(prob_base_1*prob_base_2)
        # probs_dinucleotide.append(prob_dinucleotide)
        # labels.append(key)

        ratio = prob_dinucleotide / (prob_base_1 * prob_base_2)
        dinucleotide_ratio_deviation[key] = abs(1 - ratio)

    # scatter_plot(probs_b1_and_b2, probs_dinucleotide, labels, "Probability N_1 AND N_2", "Probablility N_1N_2")
    print(max(dinucleotide_ratio_deviation, key=lambda x: dinucleotide_ratio_deviation[x]))
    print(dinucleotide_ratio_deviation)


# execute reverse comp
def execute_reverse_comp():
    # read the fasta file
    gene = geneFASTA(sys.argv[-1])

    rev_comp_gene = rev_comp(gene)

    print(gene[-100:])
    print(rev_comp_gene[:100])

def walk_genome_find_ORFS(genome, index, rf, orfs, orf_lengths):
    while (index + rf < len(genome) - 2):
        rf = (rf + 1) % 3

        codon = genome[index+rf:index+rf+3]

        if (codon == START):
            orfs[rf].append(index+rf)

        if ((codon == STOP_1) | (codon == STOP_2) | (codon == STOP_3)):
            for start in orfs[rf]:
                orf_lengths.append(((index+rf) - start) + 1)
                orfs[rf].remove(start)

        if (rf == 0):
            index += 1



def identify_ORFs():
    # read the fasta file
    gene = geneFASTA(sys.argv[-1])
    rev_comp_gene = rev_comp(gene)

    rf = 0
    index = 0
    orfs = {}
    orf_lengths = []

    for i in range(3):
        orfs[i] = []

    walk_genome_find_ORFS(gene, index, rf, orfs, orf_lengths)
    walk_genome_find_ORFS(rev_comp_gene, index, rf, orfs, orf_lengths)

    orf_data = {}
    for i in range(len(orf_lengths)):
        orf_length = orf_lengths[i]
        if (orf_length in orf_data):
            orf_data[orf_length] += 1
        else:
            orf_data[orf_length] = 1

    bar_plot_dict(orf_data, "ORF Length (bp)", "Number of ORFs", "Length and nnumber of ORF in Genome")



    # go through the gene and identify the ORF, find start codon go until stop codon
    # do same for rev comp

    # walk through gene, mark all starts and close when stop appears
    # ensure start and stop correspond to the same reading frame

    # plot dist. of ORF length

def bar_plot_dict(dict, x_title, y_title, graph_title):
    # format data for graphig
    x = list(dict.keys())
    y = list(dict.values())


    _, ax = plt.subplots()
    ax.bar(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(graph_title)
    plt.show()

def scatter_plot(x, y, labels, x_title, y_title):
    _, ax = plt.subplots()
    ax.scatter(x, y)

    for i in range(len(labels)):
        plt.text(x=x[i], y=y[i], s=labels[i])

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    # plt.title(graph_title)
    plt.show()



gene = geneFASTA(sys.argv[-1])

# (2)
# execute_reverse_comp()

# (3)
# TODO: what do you notice about nucleotide frequencies
nucleotide_freq_table = nucleotide_freq()
dinucleotide_freq_table = dinucleotide_freq()
analyze_nucleotide_dinucleotide_data(nucleotide_freq_table, dinucleotide_freq_table, len(gene))

# (4)
# TODO: how long must an ORF be to have some confidence they are not false discoveries
# identify_ORFs()
