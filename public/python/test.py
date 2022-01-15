from functools import reduce
import os
import unittest
import numpy as np
from groupRanking import agregate_judgments, agregate_priorities, multi_criterion_ranking_dict
from raportCI import generate_raport


class TestAHP(unittest.TestCase):

    # Test integralnościowy liczenia rankingu metodą AIJ
    def test_AIP(self):
        expected_rank = {'Porshe 911': 0.695925884993736, 'Ferrari Testarosa': 0.23061053415323618, 'Lamborghini Gallardo': 0.07346358085302779}
        result = np.isclose(
            list(agregate_priorities(
                3, 
                ["Porshe 911", "Ferrari Testarosa", "Lamborghini Gallardo"],
                ["fuel consumption", "design", "speed"],
                method="evm",
                mean="arithmetic",
                folder=f"test_data{os.sep}cars"
            ).values()),
            list(expected_rank.values())
        )
        self.assertTrue(self.__forall(result), f"Should all be True, got {result} instead")
    

    # Test integralnościowy liczenia rankingu metodą AIP
    def test_AIJ(self):
        expected_rank = {'Porshe 911': 0.5970905577925761, 'Ferrari Testarosa': 0.2772044599396324, 'Lamborghini Gallardo': 0.12570498226779156}
        result = np.isclose(
            list(agregate_judgments(
                3, 
                ["Porshe 911", "Ferrari Testarosa", "Lamborghini Gallardo"],
                ["fuel consumption", "design", "speed"],
                method="evm",
                mean="arithmetic",
                folder=f"test_data{os.sep}cars"
            ).values()),
            list(expected_rank.values())
        )
        self.assertTrue(self.__forall(result), f"Should all be True, got {result} instead")
    

    def test_Saaty_Harker_CI(self):
        expected_indices = {'design': 0.2669547212429493, 'fuel consumption': 0.06092772357150267, 'priorities': 0.2634980196416701, 'speed': 0.12190681147405114}
        indices = generate_raport(1, "saaty-harker", folder=f"test_data{os.sep}cars")

        for k, v in indices.items():
            self.assertAlmostEqual(
                v, 
                expected_indices[k], 
                msg=f"Saaty Harker CI for {k} is other than expected!")
    

    def test_geometric_CI(self):
        expected_indices = {'design': 0.5117129743100437, 'fuel consumption': 0.12063777037935582, 'priorities': 0.5053525280315286, 'speed': 0.2390148564292193}
        indices = generate_raport(1, "geometric", folder=f"test_data{os.sep}cars")

        for k, v in indices.items():
            self.assertAlmostEqual(
                v, 
                expected_indices[k], 
                msg=f"Geometric CI for {k} is other than expected!")
    

    def test_CR(self):
        expected_indices = {'design': 0.48892806088452245, 'fuel consumption': 0.11158923731044444, 'priorities': 0.4825971055708243, 'speed': 0.22327254848727313}
        indices = generate_raport(1, "cr", folder=f"test_data{os.sep}cars")

        for k, v in indices.items():
            self.assertAlmostEqual(
                v, 
                expected_indices[k], 
                msg=f"CR for {k} is other than expected!")
    

    def __forall(self, seq):
        return reduce(lambda x, y: x == y, seq, True)


if __name__ == "__main__":
    # unittest.main()
    rank = agregate_priorities(
        1, 
        ["Tom", "Dick", "Harry"], 
        ["Experience", "Education", "Charisma", "Age"], 
        method="geometric",
        mean="arithmetic",
        folder=f"test_data{os.sep}leader"
    )
    print(rank)

    

