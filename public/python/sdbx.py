import numpy as np
from numpy.core.fromnumeric import prod
from groupRanking import ranking_dict, fill_missing_evm
from copy import copy

def random_CP(n):
    CP = np.random.rand(n, n)
    for i in range(n):
        CP[i, i] = 1.
    for i in range(1, n):
        for j in range(0, i):
            CP[i, j] = 1 / CP[j, i]

    return CP


if __name__ == "__main__":
    CP = np.array([
        [1., 2/3, 0., 0., 9],
        [3/2, 1., 0., 7/4, 0.],
        [0., 0., 1, 0., 1/3],
        [0., 4/7, 0., 1., 9.],
        [1/9, 0., 3., 1/9, 1.]
    ])

    # print(ranking_dict(CP, ["a", "b", "c", "d", "e"], method="gmm"))
    a = [1, 2, 3, 4, 5, 6]
    print(a[:-3])
    
    
