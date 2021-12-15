import numpy as np
from math import prod
import numpy.linalg as la
import math
import os


def fill_missing_evm(cp):
    """
    Returns the fixed comparison matrix (fix works only for EVM!)
    """
    for i, row in enumerate(cp):
        s = 0
        for el in row:
            if el == 0:
                s += 1
        cp[i, i] = s + 1
    return cp


def ranking_vector_gmm(cp):
    """
    Calculates the ranking vector for a complete matrix by GMM
    """
    n = cp.shape[0]
    ranking_vec = [0 for _ in range(n)]
    for i in range(len(ranking_vec)):
        ranking_vec[i] = pow(prod(cp[i, :]), 1 / n)
    return ranking_vec


def ranking_vector_gmm_incomplete(cp):
    """
    Calculates the ranking vector for an incomplete matrix (Only for GMM!)
    """
    n = cp.shape[0]
    r = [0 for i in range(n)]
    for row in range(n):
        s = 0
        for col in range(n):
            if row != col:
                if cp[row, col] == 0:
                    s += 1
                    cp[row, col] = 1
                else:
                    r[row] += math.log(cp[row, col])
                    cp[row, col] = 0
        cp[row, row] = n - s
    r = np.array(r)
    ranking_exp = la.solve(cp, r)
    return [math.exp(w) for w in ranking_exp]


def ranking_dict(compMatrix, alternatives, method="evm"):
    """
    Calculates the ranking for alternatives based on given comparison matrix CompMatrix. The ranking
    is calculated in either eigenvector method or geometric mean method

    ### Parameters
    CompMatrix: Comparison matrix provided by expert
    alternatives: list of possible alternatives
    method: method of ranking calculation, 'evm' or 'gmm'

    ### Returns
    result: ranking dictionary
    """

    # cast comparison matrix to np.array()
    if (type(compMatrix) == type([])):
        compMatrix = np.array(compMatrix)

    if method == "evm":     # Eigenvector method

        # fix the matrix if incomplete
        compMatrix = fill_missing_evm(compMatrix)

        # w, v are eigenvalues, eigenvectors accordingly
        w, v = la.eig(compMatrix)

        # calculates the normalised ranking vector
        ranking_vec = v[:, np.argmax(w)]

        # Casts ranking vector to Real valued
        if not np.array_equal(ranking_vec, ranking_vec.astype('float')):
            print("Warning! Casting complex numbers to real with loss!")
        ranking_vec = ranking_vec.astype('float')

    else:                   # Geometric mean method

        if compMatrix.__contains__(0):      # case of incomplete matrix
            ranking_vec = ranking_vector_gmm_incomplete(compMatrix)
        else:                               # case of complete matrix
            ranking_vec = ranking_vector_gmm(compMatrix)

    # Softmax
    ranking_vec = ranking_vec / np.sum(ranking_vec)

    # Creates dictionary from alternatives and according wages from ranking vector
    ranking = dict(zip(alternatives, ranking_vec))
    return dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))


def multi_criterion_ranking_dict(CompMatrices, CritCompMatrix, alternatives, criteria, method="evm"):
    res = {alt: 0 for alt in alternatives}

    criteria_ranking_dict = ranking_dict(CritCompMatrix, criteria, method=method)

    for i, criterium in enumerate(criteria):
        rank_for_crit = ranking_dict(CompMatrices[i], alternatives, method=method)

        for alt in alternatives:
            res[alt] += rank_for_crit[alt] * criteria_ranking_dict[criterium]  # czemu nie res[alt] = ...?

    return res


def agregate_judgments(no_experts, alternatives, criteria, method="evm", mean="arithmetic"):
    """
    Calculates ranking based on aggregation of individual judgments (AIJ)

    ### Parameters
    no_experts: number of experts that had been surveed
    alternatives: list of possible alternatives
    criteria: list of criteria in respect to which we calculate ranking
    method: method of ranking calculation, 'evm' or 'gmm'
    mean: the type of mean applied in agregation (arithmetic or geometric), arithmetic by default

    ### Returns
    result: dictionary representing ranking, sorted in descending order
    """

    sep = os.sep

    CPs = {c: [
        np.loadtxt(f"public{sep}python{sep}matrices{sep}{c}_exp{exp}.txt") for exp in range(1, no_experts)
    ] for c in criteria}
    priorities = [
        np.loadtxt(f"public{sep}python{sep}matrices{sep}priorities_exp{exp}.txt") for exp in range(1, no_experts)
    ]

    agregatedCPs = [
        prod(matrices, start=np.ones((len(alternatives), len(alternatives)))) for matrices in CPs.values()
    ]
    agregatedCPs = [pow(agregatedCPs[i], 1 / no_experts) for i in range(len(criteria))]
    agregatedPriorities = prod(priorities, start=np.ones((len(alternatives), len(alternatives))))
    agregatedPriorities = pow(agregatedPriorities, 1 / no_experts)

    final_ranking = multi_criterion_ranking_dict(
        agregatedCPs,
        agregatedPriorities,
        alternatives,
        criteria,
        method
    )

    return dict(sorted(final_ranking.items(), key=lambda it: it[1], reverse=True))


def agregate_priorities(no_experts, alternatives, criteria, method="evm", mean="arithmetic"):
    """
    Calculates ranking based on aggregation of individual priorities (AIP)

    ### Parameters
    no_experts: number of experts that had been surveed
    alternatives: list of possible alternatives
    criteria: list of criteria in respect to which we calculate ranking
    method: method of ranking calculation, 'evm' or 'gmm'
    mean: the type of mean applied in agregation (arithmetic or geometric), arithmetic by default

    ### Returns
    result: dictionary representing ranking, sorted in descending order
    """

    sep = os.sep

    # Dictionary of 'expert index' -> 'comparison matrices list' pairs
    CPs = {exp: [
        np.loadtxt(f"public{sep}python{sep}matrices{sep}{c}_exp{exp}.txt") for c in criteria
    ] for exp in range(1, no_experts + 1)}

    # list of rankings from every expert
    judgments = {exp: multi_criterion_ranking_dict(
        CPs[exp],
        np.loadtxt(f"public{sep}python{sep}matrices{sep}priorities_exp{exp}.txt"),
        alternatives,
        criteria,
        method=method
    ) for exp in range(1, no_experts + 1)}

    # Agregate rankings
    final_ranking = {alt: 0 for alt in alternatives}
    if mean == "arithmetic":
        for exp in range(1, no_experts + 1):
            for alt in alternatives:
                final_ranking[alt] += judgments[exp][alt]
        for alt in alternatives:
            final_ranking[alt] = final_ranking[alt] / no_experts
    else:
        for alt in alternatives:
            final_ranking[alt] = 1
        for exp in range(1, no_experts + 1):
            for alt in alternatives:
                final_ranking[alt] *= judgments[exp][alt]
        for alt in alternatives:
            final_ranking[alt] = pow(final_ranking[alt], 1 / no_experts)

    return dict(sorted(final_ranking.items(), key=lambda it: it[1], reverse=True))




if __name__ == "__main__":
    # no_exp = 4
    # criterias = ["size", "design", "speed"]
    # cars = ["lambo", "ferrari", "porshe"]
    # ranking = agregate_priorities(no_exp, cars, criterias, method="gmm")
    # print(ranking)
    # print(sum(ranking.values()))

    no_exp = 2
    criterias = ['a', 'b', 'c']
    cars = ["1", "2", "3"]
    ranking = agregate_priorities(no_exp, cars, criterias, method="evm")
    print(ranking)
    print(f"Ranking sums to {sum(ranking.values())}")
