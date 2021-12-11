import numpy as np

def random_CP(n):
    CP = np.random.rand(n, n)
    for i in range(n):
        CP[i, i] = 1.
    for i in range(1, n):
        for j in range(0, i):
            CP[i, j] = 1 / CP[j, i]

    return CP


if __name__ == "__main__":
    print(pow(8, 1 / 5))
    
