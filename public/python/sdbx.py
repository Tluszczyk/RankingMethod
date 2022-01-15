import numpy as np
from numpy.core.fromnumeric import prod
from groupRanking import ranking_dict, fill_missing_evm
from matrix_factory import random_CP
from copy import copy


if __name__ == "__main__":
    np.random.seed(2137)
    cp = random_CP(5)
    print(cp)

    
    
