
# 一阶差分

import numpy as np


def difference(data):
    start = np.array([0])
    return np.append(start, np.diff(data))
