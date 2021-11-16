import sys

import numpy as np
import numpy.linalg as la

from functools import reduce

def ranking_dict(CompMatrix, alternatives):
    """
    Calculates the ranking for alternatives based on given comparison matrix CompMatrix
    :returns: ranking dictionary
    """

    # w, v are eigenvalues, eigenvectors accordingly
    w, v = la.eig(CompMatrix)

    # calculates the normalised ranking vector
    ranking_vec = v[:, np.argmax(w)]

    # Casts ranking vector to Real valued
    if not np.array_equal(ranking_vec, ranking_vec.astype('float')):
        print("Warning! Casting complex numbers to real with loss!")
    ranking_vec = ranking_vec.astype('float')

    # Softmax
    ranking_vec = ranking_vec / np.sum(ranking_vec)

    # Creates dictionary from alternatives and according wages from ranking vector
    ranking = dict(zip(alternatives, ranking_vec))
    return dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))


matrix_s = sys.argv[1]
alternatives_s = sys.argv[2]

# matrix_s = "1,0.66,2,1.5,1,2,0.5,0.5,1"
# alternatives_s = "UJ,AGH,PWR"

alternatives = alternatives_s.split(',')

N = len(alternatives)

matrix = np.reshape(
    list(
        map(
            lambda x: float(x),
            matrix_s.split(',')
        )
    ),
    (N, N)
).tolist()

# ranking_str = ""

# rank = ranking_dict(matrix, alternatives)
# for key in sorted(rank, key=lambda e: e[1]):
#     ranking_str += key + ":" + str(rank[key]) + ","

# print(ranking_str[:-1])

print(ranking_dict(matrix, alternatives))
sys.stdout.flush()