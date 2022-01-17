import sys

import json
import numpy as np
from math import sqrt

from raportCI import *

import warnings
warnings.filterwarnings("ignore")

matrix_s, method = sys.argv[1:3]

l = int(sqrt(len(matrix_s.split(','))))

matrix = np.array(matrix_s.split(','), float).reshape(l,l)

ci = None
cr = None

if method == 'evm':
    ci = saaty_harker_CI(matrix)
    cr = consistancy_ratio(matrix)

elif method == 'gmm':
    ci = geometric_CI(matrix)

print(f'{ci} {cr}', end="")

sys.stdout.flush()