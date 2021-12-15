import sys

import numpy as np
import numpy.linalg as la

from functools import reduce

from groupRanking import *

# input from parent process
alternatives_s, criteria_s = sys.argv[1:3]
method, expertsNum = sys.argv[3:5]

# data preprocessing String -> [[[Float]]]
alternatives = alternatives_s.split(',')
criteria = criteria_s.split(',')

# N = len(alternatives)

# comparations = np.reshape(
#     list(map(float, comparations_s.split(','))),
#     (len(criteria),N,N)
# ).tolist()

# criteriaComparations = np.reshape(
#     list(map(float, criteriaComparations_s.split(','))),
#     (len(criteria),len(criteria))
# ).tolist()

# building ranking from many criteria
# final_ranking_dict = multi_criterion_ranking_dict(
#     comparations,
#     criteriaComparations,
#     alternatives,
#     criteria
# )

# print(expertsNum)
# print(alternatives)
# print(criteria)
# print(method)

final_ranking_dict = agregate_priorities(int(expertsNum),
                                         alternatives,
                                         criteria,
                                         method=method)



print(final_ranking_dict)
sys.stdout.flush()