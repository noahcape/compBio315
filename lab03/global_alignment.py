
# scoring policy for global alignment
GAP = -2

# optimize scoring for DNA if tranversion or transition is cause for mismatch
MATCH = lambda str_1, str_2, i, j: 1 if str_1[i] == str_2[j] else -1

# initialize matrix
def init_matrix_global(len_1, len_2):
    # initialize matrix with length + 1 for the two strings lengths
    matrix = [ [0 for _ in range(len_2 + 1)] for _ in range(len_1 + 1)]

    for i in range(1, len_1 + 1):
        matrix[i][0] = matrix[i-1][0] + GAP

    for j in range(1, len_2 + 1):
        matrix[0][j] = matrix[0][j-1] + GAP

    return matrix
    

# walk the matrix and score the matrix
def score_matrix(str_1, str_2, a, local = False):
    for i in range(1, len(str_1) + 1):
        for j in range(1, len(str_2) + 1):
            # generate the possible new optimal score
            s_1 = a[i-1][j-1] + MATCH(str_1, str_2, i - 1, j - 1)
            s_2 = a[i][j-1] + GAP
            s_3 = a[i-1][j] + GAP

            scores = [s_1, s_2, s_3]
            if (local):
                scores.append(0)

            # choose the best of the scores
            a[i][j] = max(scores)

def back_trace(str_1, str_2, a, local, init_i = -1, init_j = -1):
    cons_str_1 = ""
    cons_str_2 = ""

    i = len(str_1) if not local else init_i
    j = len(str_2) if not local else init_j

    condition = lambda i, j: (i > 0) | (j > 0) if not local else (a[i][j] != 0)

    while (condition(i, j)):
        # get possible spaces to trace back to
        s_1 = a[i-1][j-1]
        s_2 = a[i][j-1]
        s_3 = a[i-1][j]

        s = a[i][j]

        # compare possible trace back spaces to with current score
        # when one matches take that route
        if ((s - MATCH(str_1, str_2, i - 1, j - 1)) == s_1):
            cons_str_1 = str_1[i - 1] + cons_str_1
            cons_str_2 = str_2[j - 1] + cons_str_2
            i -= 1
            j -= 1
        elif ((s - GAP) == s_2):
            cons_str_1 = "_" + cons_str_1
            cons_str_2 = str_2[j - 1] + cons_str_2
            j -= 1
        elif ((s - GAP) == s_3):
            cons_str_1 = str_1[i - 1] + cons_str_1
            cons_str_2 = "_" + cons_str_2
            i -= 1
        else:
            print("SOMETHING WENT WRONG")
            return -1  

    print(cons_str_1)
    print(cons_str_2)

# print the matrix
def print_matrix(a):
    for i in range(len(a)):
        print(a[i])



def align_seqs(seq1, seq2):
    # initialize matrix
    matrix = init_matrix_global(len(seq1), len(seq2))

    # score matrix
    score_matrix(seq1, seq2, matrix)

    # return the score
    return matrix[len(seq1)][len(seq2)]


