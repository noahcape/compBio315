import matplotlib.pyplot as plt
from dpa_funcs import geneFASTA
import sys

START = "ATG"
STOP = ["TAA", "TAG", "TGA"]

SEQ_BASES = "ATGC"


# take string gene and return reverse complement
def rev_comp(gene):
    # reverse the gene
    gene = gene[::-1]

    # create mapping of complements
    table = gene.maketrans(SEQ_BASES, SEQ_BASES)

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
def nucleotide_freq(gene):
    # generate empty dictionary
    freq_dict = generate_dict(SEQ_BASES, 1)
    print(freq_dict)

    # read base by base of gene
    for i in range(len(gene)):
        base = gene[i]
        if (base in freq_dict):
            freq_dict[base] += 1

    return freq_dict

# read gene and keep track of dinucleotide freq in dictionary
def dinucleotide_freq(gene, is_circular = False):
    # generate empty dict for dinucleotide
    freq_dict = generate_dict(SEQ_BASES, 2)


    # read through gene
    for i in range(len(gene) - 1):
        dinucleotide = gene[i:i+2]
        if (dinucleotide in freq_dict):
            freq_dict[dinucleotide] += 1    

    if is_circular:
        dinucleotide = gene[-1] + gene[0]
        if (dinucleotide in freq_dict):
            freq_dict[dinucleotide] += 1

    return freq_dict

# note that is genome is linear and genome size is n, num dinucleotides is n-1
def analyze_nucleotide_dinucleotide_data(nucleotide_freqs, dinucleotide_freqs, genome_size):
    # determine which dinucleotide most differs from chance they appear together per genomes base frequency
    dinucleotide_ratio_deviation = generate_dict(SEQ_BASES, 2)

    genome_size_wo_unkowns = sum(map(lambda x: nucleotide_freqs[x], nucleotide_freqs))

    for key in dinucleotide_ratio_deviation:
        base_1 = key[0]
        base_2 = key[1]

        # calculate probabilities
        prob_base_1 = nucleotide_freqs[base_1] / genome_size_wo_unkowns
        prob_base_2 = nucleotide_freqs[base_2] / genome_size_wo_unkowns
        prob_dinucleotide = dinucleotide_freqs[key] / genome_size_wo_unkowns

        ratio = prob_dinucleotide / (prob_base_1 * prob_base_2)
        dinucleotide_ratio_deviation[key] = abs(1 - ratio)

    print("Most significant dinucleotide:", max(dinucleotide_ratio_deviation, key=lambda x: dinucleotide_ratio_deviation[x]))
    print({b: round((nucleotide_freqs[b]/genome_size)*100, 4) for b in list(nucleotide_freqs.keys())})
    

# walk the geneome and find ORFs in the three reading frames
def walk_genome_find_ORFS(genome, index, rf, orfs, orf_lengths):
    while (index < (len(genome) - 2)):
        # keep track of the reading frame
        rf = index % 3

        # take the current codon
        codon = genome[index:index+3]

        # if its a start keep track of its position
        if (codon == START):
            orfs[rf].append(index)

        # if it is a possible stop codin
        if (codon in STOP):
            # close all open reading frames in current rf
            for start in orfs[rf]:
                orf_lengths.append((index - start) + 1)                
                orfs[rf].remove(start)

        index+=1


# function to identify ORFs with in a gene (major and minor strand)
def identify_ORFs():
    rev_comp_gene = rev_comp(gene)

    orfs = {}
    orf_lengths = []

    # count each reading frame at the same time walking through the gene
    for i in range(3):
        # each list in the dict keeps track of one reading frame
        orfs[i] = []

    # start by walking major strand
    walk_genome_find_ORFS(gene, 0, 0, orfs, orf_lengths)

    # start new, remove unclosed ORFs for rev-com analysis
    for i in range(3):
        orfs[i] = []
    
    # walk the reverse complement strand
    walk_genome_find_ORFS(rev_comp_gene, 0, 0, orfs, orf_lengths)

    # to store the length and number of ORFs of that length
    orf_data = {}

    # count up ORFs of each length to plot
    for i in range(len(orf_lengths)):
        orf_length = orf_lengths[i]
        if (orf_length in orf_data):
            orf_data[orf_length] += 1
        else:
            orf_data[orf_length] = 1


    # show some confidence in ORF len
    calculate_probability(orf_data, len(gene))
    
    # plot
    bar_plot_dict(orf_data, "ORF Length (bp)", "Number of ORFs", "Length and number of ORF in Genome")

def bar_plot_dict(dict, x_title, y_title, graph_title):
    # format data for graphig
    x = list(dict.keys())
    y = list(dict.values())


    _, ax = plt.subplots()
    ax.bar(x, y, width=2)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(graph_title)
    plt.show()

# calculate probability of this ORF showing up using chi square test
def calculate_probability(orf_data, genome_size):
    # probability that ORF of length n exists
    p_of_ORF_len_n = lambda n: pow((1 - (3 / 64)), n)

    max_reject = 0
    for len in orf_data:
        # expected number of orf of len
        expected = p_of_ORF_len_n(len) * genome_size

        # number of orfs observed
        observed = orf_data[len]

        if (expected > 0):
            chi_square = (pow((observed - expected), 2) / expected)

            if (chi_square < 3.841):
                if (len > max_reject):
                    max_reject = len

    if (max_reject > 0):
        print("Confidence if ORF is longer than", max_reject)


gene = geneFASTA(sys.argv[-2])
circular = sys.argv[-1] == -1

# (2)
rev_comp_gene = rev_comp(gene)

print(gene[:100])
print(rev_comp_gene[:100])

# (3)
nucleotide_freq_table = nucleotide_freq(gene)
dinucleotide_freq_table = dinucleotide_freq(gene, circular)
analyze_nucleotide_dinucleotide_data(nucleotide_freq_table, dinucleotide_freq_table, len(gene))

# (4)
identify_ORFs()
