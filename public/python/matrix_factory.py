import numpy as np
import os


def random_CP(n):
    CP = np.random.rand(n, n)
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


def generate_CPs(no_alternatives, criteria, no_experts):
    names = [[f"{c}_exp{exp}" for exp in range(1, no_experts + 1)] for c in criteria]
    names = [n for c in names for n in c]
    clear_dir("public\\python\\matrices")

    for n in names:
        np.save(f"public\\python\\matrices\\{n}.npy", random_CP(no_alternatives))
    
    for exp in range(1, no_experts + 1):
        np.save(f"public\\python\\matrices\\priorities_exp{exp}.npy", random_CP(len(criteria)))
    


if __name__ == "__main__":
    confirm = input("Do you really want to generate random matrices? [y/n]\n")
    if confirm == "y":
        generate_CPs(3, ["size", "design", "speed"], 4)