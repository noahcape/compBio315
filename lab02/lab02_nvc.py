# implementing the Needleman-Wunsch global alignment algorithm

# scoring policy for global alignment
GAP = -2
MATCH = lambda str_1, str_2, i, j: 1 if str_1[i] == str_2[j] else -1

# initialize matrix
def init_matrix(len_1, len_2):
    # initialize matrix with length + 1 for the two strings lengths
    matrix = [ [0 for _ in range(len_2 + 1)] for _ in range(len_1 + 1)]

    for i in range(1, len_1 + 1):
        matrix[i][0] = matrix[i-1][0] - 2

    for j in range(1, len_2 + 1):
        matrix[0][j] = matrix[0][j-1] - 2

    return matrix

# walk the matrix and score the matrix
def score_matrix(str_1, str_2, a):
    for i in range(1, len(str_1) + 1):
        for j in range(1, len(str_2) + 1):
            s_1 = a[i-1][j-1] + MATCH(str_1, str_2, i - 1, j - 1)
            s_2 = a[i][j-1] + GAP
            s_3 = a[i-1][j] + GAP

            a[i][j] = max([s_1, s_2, s_3])

def back_trace(str_1, str_2, a):
    cons_str_1 = ""
    cons_str_2 = ""

    i = len(str_1)
    j = len(str_2)

    while ((i > 0) | (j > 0)):
        s_1 = a[i-1][j-1]
        s_2 = a[i][j-1]
        s_3 = a[i-1][j]

        s = a[i][j]

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

STRING_1 = "LOCALLY"
STRING_2 = "GLOBAL"

a = init_matrix(len(STRING_1), len(STRING_2))
score_matrix(STRING_1, STRING_2, a)

print_matrix(a)

back_trace(STRING_1, STRING_2, a)


