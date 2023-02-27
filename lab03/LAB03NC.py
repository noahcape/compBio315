# Method for identifying repetative elements in HUGE search string
# use FASTA method for identifying best diagonal to align
# for each seed check the best start stops from FASTA analysis
# use gappless extension like BLAST

import sys
from dpa_funcs import geneFASTA
import matplotlib.pyplot as plt
import pickle
from global_alignment import align_seqs

DB = geneFASTA(sys.argv[-1])
QUERY = "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGACCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAATACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCAGCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGGAGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCCAGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAAAAA"

K = 6
NUM_OFFSETS = 1000

MISMATCH = -1
MATCH = 1

# store position for each ktup
ktup_table = {}
# calculate offsets
offset_vector_dict = {}

# vector to store positions of matches
match_pos_vector = []

def write_obj_to_file(filename, obj):
    # create a binary pickle file 
    f = open('{0}.pkl'.format(filename),"wb")

    # write the python object (dict) to pickle file
    pickle.dump(obj, f)

    # close file
    f.close()

def read_file(filename):
    obj = []

    with(open('{0}.pkl'.format(filename), "rb")) as file:
        while True:
            try:
                obj = pickle.load(file)
            except EOFError:
                break

    return obj

def graph_data(x, y, x_title, y_title, title):
    _, ax = plt.subplots()
    ax.bar(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.show()


def gapless_score(s, t, k, display=False):
    score = 0
    match_str = ""
    for i in range(len(s)):
        if (s[i] == t[i+k]):
            score += MATCH
            match_str+= "|"
        else:
            score += MISMATCH
            match_str+="~"

    if display:
        print("Score:", score)
        # print(s)
        # print(match_str)
        # print(t[k:k+len(s)])
        # return t[k:k+len(s)]
    return score

def build_ktup_table(k, db):
    for i in range(len(db) - k):
        ktup = db[i:i+k]
        if (ktup in ktup_table):
            ktup_table[ktup].append(i)
        else:
            ktup_table[ktup] = [i]

def build_offset_table(k, query):
    for t in range(len(query) - k):
        ktup = query[t:t+k]

        # determine if the db_ktup is a match if gapless extension is pretty good
        for db_ktup in ktup_table:
            if (gapless_score(ktup, db_ktup, 0) > (k*0.5)):
                for s in ktup_table[db_ktup]:
                    offset = s - t
                    offset_vector_dict[offset] = offset_vector_dict.get(offset, 0) + 1

    # having a good hit a some pos. means next len(Alu) are prob bad matches
    best_n = sorted(
        offset_vector_dict, 
        key=lambda key: offset_vector_dict[key], reverse=True)[:NUM_OFFSETS]

    write_obj_to_file("best_n_offsets", best_n)
    return best_n

def build_tup_dict(bands):
    matches = []
    scores = []

    for i in range(len(QUERY) - K):
        seed = QUERY[i:i+K]
        for b in bands:
            db_index = b-i
            db_seq = DB[db_index:db_index+K]

            # ensuring that the gapless score of the seed and db_seq is good ensure unique matches
            if (db_index + (len(QUERY) - i) < len(DB) and db_index - (len(QUERY) - i) > 0 and gapless_score(seed, db_seq, 0) > 0):
                score = 0
                match = DB[db_index: db_index+len(QUERY)]

                score = align_seqs(QUERY, match)

                matches.append(match)
                scores.append(score)
                
                
    write_obj_to_file("match_scores_sw_4", scores)
    write_obj_to_file("alu_matches_sw_4", matches)
    return matches

def determine_overlaps(match_positions):
    min_overlap = len(QUERY) / 3

    for match in match_positions:
        (start_a, _) = match

        for other_match in match_positions:
            if match == other_match:
                break

            (start_b, _) = other_match
            start_diff = abs(start_b - start_a)

            if (start_diff < min_overlap):
                print(match, other_match)

    return False

def format_score_data(scores):
    dict = {}

    for s in scores:
        dict[s] = dict.get(s, 0) + 1

    return dict



# ktup_table = {}
# # calculate offsets
# offset_vector_dict = {}
# build_ktup_table(K, DB)
# diagonals = build_offset_table(K, QUERY)

# diagonals = read_file("best_n_offsets")

# matches = build_tup_dict(diagonals)
# print(NUM_OFFSETS, len(matches))

# read and print out graph of scores
scores = read_file("match_scores_sw_4")
print(len(scores))
scores_dict = format_score_data(scores)
graph_data(scores_dict.keys(), scores_dict.values(), "SW Global Alignment", "Number of Matches with Score", "Number of matches with given score")


# file:
# match_score_3.pkl
    # determines seed offsets with gapless extension not exact match (takes a bit more time bu gapless extension is fast)
