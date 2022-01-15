import numpy as np
import os


def random_CP(n):
    CP = np.random.rand(n, n) * 9
    for i in range(n):
        CP[i, i] = 1.
    for i in range(1, n):
        for j in range(0, i):
            CP[i, j] = 1 / CP[j, i]

    return CP


def clear_dir(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        os.remove(file_path)
    pass


def generate_CPs(no_alternatives, criteria, no_experts, folder='matrices'):
    sep = os.sep
    names = [[f"{c}_exp{exp}" for exp in range(1, no_experts + 1)] for c in criteria]
    names = [n for c in names for n in c]
    clear_dir(f"public{sep}python{sep}{folder}")

    for n in names:
        np.savetxt(f"public{sep}python{sep}{folder}{sep}{n}.txt", random_CP(no_alternatives))
    
    for exp in range(1, no_experts + 1):
        np.savetxt(f"public{sep}python{sep}{folder}{sep}priorities_exp{exp}.txt", random_CP(len(criteria)))
    


if __name__ == "__main__":
    np.random.seed(2137)
    confirm = input("Do you really want to generate random matrices? [y/n]\n")
    if confirm == "y":
        generate_CPs(3, ["Experience", "Education", "Charisma", "Age"], 1, folder=f"test_data{os.sep}leader")

    