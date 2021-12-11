import numpy as np
import numpy.linalg as la


def ranking_dict(CompMatrix, alternatives):
    """
    Calculates the ranking for alternatives based on given comparison matrix CompMatrix
    returns: ranking dictionary
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
            res[alt] += rank_for_crit[alt] * criteria_ranking_dict[criterium]  # czemu nie res[alt] = ...? 

    return res

def agregate_priorities(no_experts, alternatives, criteria, mean="arithmetic"):
    """
    Calculates ranking based on aggregation of individual priorities (AIP)

    ### Parameters
    no_experts: number of experts that had been surveed
    alternatives: list of possible alternatives
    criteria: list of criteria in respect to which we calculate ranking
    mean: the type of mean applied in agregation (arithmetic or geometric), arithmetic by default

    ### Returns
    result: dictionary representing ranking, sorted in descending order
    """

    # Dictionary of 'expert index' -> 'comparison matrices list' pairs
    CPs = {exp: [
        np.load(f"public\\python\\matrices\\{c}_exp{exp}.npy") for c in criteria
    ] for exp in range(1, no_experts + 1)}

    # list of rankings from every expert
    judgments = {exp: multi_criterion_ranking_dict(
        CPs[exp], 
        np.load(f"public\\python\\matrices\\priorities_exp{exp}.npy"),
        alternatives,
        criteria
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
    no_exp = 4
    criterias = ["size", "design", "speed"]
    cars = ["lambo", "ferrari", "porshe"]
    ranking = agregate_priorities(no_exp, cars, criterias, mean="arithmetic")
    print(ranking)