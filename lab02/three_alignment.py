THREE_MATCH = lambda s_1, s_2, s_3, i, j, k: 3 if (s_1[i] == s_2[j]) & (s_1[i] == s_3[k]) else -1
TWO_MATCH = lambda s_1, s_2, i, j: 1 if (s_1[i] == s_2[j]) else -1
THREE_GAP = -3

def init_matrix_three_alignment(str_1, str_2, str_3):
    matrix = [ [[0 for _ in range(len(str_3) + 1)] for _ in range(len(str_2) + 1)] for _ in range(len(str_1) + 1)]

    for i in range(1, len(str_1) + 1):
        matrix[i][0][0] = matrix[i - 1][0][0] + THREE_GAP

    for j in range(1, len(str_2) + 1):
        matrix[0][j][0] = matrix[0][j - 1][0] + THREE_GAP
    
    for k in range(1, len(str_3) + 1):
        matrix[0][0][k] = matrix[0][0][k - 1] + THREE_GAP

    return matrix

def score_three_matrix(str_1, str_2, str_3, a):
    for i in range(1, len(str_1) + 1):
        for j in range(1, len(str_2) + 1):
            for k in range(1, len(str_3) + 1):
                s_1a = a[i-1][j-1][k-1] + THREE_MATCH(str_1, str_2, str_3, i - 1, j - 1, k - 1)
                s_1b = a[i-1][j][k-1] + TWO_MATCH(str_1, str_3, i-1, k-1)
                s_1c = a[i][j-1][k-1] + TWO_MATCH(str_2, str_3, j-1, k-1)
                s_1d = a[i-1][j-1][k] + TWO_MATCH(str_1, str_2, i-1, j-1)
                s_2a = a[i][j-1][k] + THREE_GAP
                s_2b = a[i-1][j][k] + THREE_GAP
                s_2c = a[i][j-1][k-1] + THREE_GAP

                print(a[i][j])

                a[i][j][k] = max([s_1a, s_2a, s_2b, s_2c, s_1b, s_1c, s_1d])

def back_trace_three(str_1, str_2, str_3, a):
    cons_str_1 = ""
    cons_str_2 = ""
    cons_str_3 = ""

    i = len(str_1)
    j = len(str_2)
    k = len(str_3)

    while((i > 0) | (j > 0) | (k > 0)):
        s_1 = a[i - 1][j - 1][k - 1]
        s_2 = a[i - 1][j][k]
        s_3 = a[i][j - 1][k]
        s_4 = a[i][j][k - 1]

        s = a[i][j][k]

        if ((s - THREE_MATCH(str_1, str_2, str_3, i - 1, j - 1, k - 1)) == s_1):
            cons_str_1 = str_1[i - 1] + cons_str_1
            cons_str_2 = str_2[j - 1] + cons_str_2
            cons_str_3 = str_3[k - 1] + cons_str_3
            i -= 1
            j -= 1
            k -= 1
        elif ((s - THREE_GAP) == s_2):
            cons_str_1 = "_" + cons_str_1
            cons_str_2 = str_2[j - 1] + cons_str_2
            cons_str_3 = str_3[k - 1] + cons_str_3
            i -= 1
        elif ((s - THREE_GAP) == s_3):
            cons_str_1 = str_1[i - 1] + cons_str_1
            cons_str_2 = "_" + cons_str_2
            cons_str_3 = str_3[k - 1] + cons_str_3
            j -= 1
        elif ((s - THREE_GAP) == s_4):
            cons_str_1 = str_1[i - 1] + cons_str_1
            cons_str_2 = str_2[j - 1] + cons_str_2
            cons_str_3 = "_" + cons_str_3
            k -= 1
        else:
            print("SOMETHING WENT WRONG")
            return -1  

    print(cons_str_1)
    print(cons_str_2)
    print(cons_str_3)


def print_matrix(a):
    for i in range(len(a)):
        print(a[i])


STRINGS = ["LOCALLY", "GLOBAL", "LOCAL"]
a_three = init_matrix_three_alignment(STRINGS[0], STRINGS[1], STRINGS[2])
score_three_matrix(STRINGS[0], STRINGS[1], STRINGS[2], a_three)
print_matrix(a_three)
back_trace_three(STRINGS[0], STRINGS[1], STRINGS[2], a_three)