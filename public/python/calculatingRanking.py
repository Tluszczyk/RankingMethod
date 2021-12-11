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


def multi_criterion_ranking_dict(CompMatrices, CritCompMatrix, alternatives, criteria):
    res = {alt: 0 for alt in alternatives}

    criteria_ranking_dict = ranking_dict(CritCompMatrix, criteria)

    for i, criterium in enumerate(criteria):
        rank_for_crit = ranking_dict(CompMatrices[i], alternatives)

        for alt in alternatives:
            res[alt] += rank_for_crit[alt] * criteria_ranking_dict[criterium]

    return res

# examples
alternatives_s = "1,2,3"
criteria_s = "a,b,c"
comparations_s = "\
1,1,1,\
1,1,1,\
1,1,1,\
\
1,1,2,\
1,1,3,\
.5,.33,1,\
\
1,4,5,\
.25,1,6,\
.2,.166,1"

criteriaComparations_s = "\
1,2,2,\
.5,1,2,\
.5,.5,1\
"

# input from parent process
alternatives_s, criteria_s, comparations_s, criteriaComparations_s = sys.argv[1:5]


# data preprocessing String -> [[[Float]]]

alternatives = alternatives_s.split(',')
criteria = criteria_s.split(',')

N = len(alternatives)

comparations = np.reshape(
    list(map(float, comparations_s.split(','))),
    (len(criteria),N,N)
).tolist()

criteriaComparations = np.reshape(
    list(map(float, criteriaComparations_s.split(','))),
    (len(criteria),len(criteria))
).tolist()

# building ranking from many criteria
final_ranking_dict = multi_criterion_ranking_dict(
    comparations,
    criteriaComparations,
    alternatives,
    criteria
)

print(final_ranking_dict)
sys.stdout.flush()