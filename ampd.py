
# AMPD算法寻找极值
# 来源：https://zhuanlan.zhihu.com/p/549588865

import numpy as np


def AMPD(data):
    """
    实现AMPD算法
    :param data: 1-D numpy.ndarray
    :return: 波峰所在索引值的列表
    """
    p_data = np.zeros_like(data, dtype=np.int32)
    count = data.shape[0]
    arr_rowsum = []
    """
    50是个可调参数，方法还需要调整
    """
    for k in range(1, count // 100 + 1):
        row_sum = 0
        for i in range(k, count - k):
            if data[i] >= data[i - k] and data[i] > data[i + k]:
                row_sum -= 1
        arr_rowsum.append(row_sum)
    min_index = np.argmin(arr_rowsum)
    max_window_length = min_index
    for k in range(1, max_window_length + 1):
        for i in range(k, count - k):
            if data[i] >= data[i - k] and data[i] > data[i + k]:
                p_data[i] += 1
    return np.where(p_data == max_window_length)[0]
