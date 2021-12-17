import numpy as np
import numpy.linalg as la
import math
import os
import re
from copy import copy
from groupRanking import fill_missing_evm, ranking_vector_gmm, ranking_vector_gmm_incomplete


def saaty_harker_CI(cp):
    fill_missing_evm(cp)
    n = cp.shape[0]
    w, _ = la.eig(cp)
    return (max(w).astype('float') - n) / (n - 1)


def consistancy_ratio(cp, q=9):
    # Temporarly we have correct table only for q = 9
    q = 9
    sep = os.sep
    cr_table = np.loadtxt(f"public{sep}python{sep}CR_table.txt")
    r = cr_table[q - 3, cp.shape[0] - 3]
    return saaty_harker_CI(cp) / r


def geometric_CI(cp):

    # Firstly, we calculate ranking (Again...)
    if cp.__contains__(0):              # case of incomplete matrix
        ranking = ranking_vector_gmm_incomplete(copy(cp))
    else:                               # case of complete matrix
        ranking = ranking_vector_gmm(copy(cp))
    
    # And now we can use ranking to calculate CI
    n = cp.shape[0]
    errors = []
    for j in range(n):
        for i in range(j):
            if cp[i, j] != 0:
                errors.append(cp[i, j] * (ranking[j] / ranking[i]))
    errors = [math.pow(math.log(e), 2) for e in errors]
    return sum(errors) / len(errors)


def generate_raport(expertID, method):
    """
    Generates raport file with every comparison matrix Consistency Index CI form
    individual expert

    ### Parameters
    expertID: an id of the analized experts matrices
    method: the method used to calculate consistency index
    """

    sep = os.sep
    sufLen = len(f"_exp{expertID}.txt")
    regex = f".*_exp{expertID}\.txt"

    # creating a dictinary of comparison matrix name - np.array pair
    matrices = {}
    for root, dirs, files in os.walk(f"public{sep}python{sep}matrices"):
        for f in files:
            if re.findall(regex, f):
                matrices[f[:-sufLen]] = np.loadtxt(os.path.join(root, f))
    
    # Choose apropiate method of calculation
    if method == "saaty-harker":
        indices = {k: saaty_harker_CI(matrices[k]) for k in matrices.keys()}
    elif method == "CR":
        indices = {k: consistancy_ratio(matrices[k]) for k in matrices.keys()}
    elif method == "geometric":
        indices = {k: geometric_CI(matrices[k]) for k in matrices.keys()}
    else:
        raise ValueError(
            "Unhandled argument value in generate_raport(), use one of [saaty-harker, geometric, CR]"
            )

    return indices

if __name__ == "__main__":
    print("Raport Generating Module")
    ind = generate_raport(3, "geometric")
    print(ind)

