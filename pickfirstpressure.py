
# 寻找初撑点

import numpy as np
from difference import difference


def pickFirstPressure(y, index):

    y_diff = difference(np.log2(y+0.001))

    first_index_list = []

    for i in range(0, len(index)):

        step = 20

        if i != len(index) - 1 and index[i + 1] - index[i] <= 10:
            step = int((index[i + 1] - index[i]))

        for j in range(index[i], index[i] + step):
            if abs(y_diff[j]) < 0.5 and y[j] > 10:
                first_index = j
                break

        first_index_list.append(first_index)

    return first_index_list
