
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

from ampd import AMPD
from difference import difference
from pickendpressure import pickEndPressure
from pickfirstpressure import pickFirstPressure


def sim_data():
    """
    N = 1000
    x = np.linspace(0, 200, N)
    y = 2 * np.cos(2 * np.pi * 300 * x) \
        + 5 * np.sin(2 * np.pi * 100 * x) \
        + 4 * np.random.randn(N)
    return y
    """
    x = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 2, 2, 1, 1, 1, 2,
         2, 3, 3, 2, 2, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1]
    y = np.array(x)
    return y


def read_excle():
    data = pd.read_excel(io=r'D:\1 工作文件\19 A+计划矿压分析\Temp.xlsx')
    return np.array(list(data.pressure))


if __name__ == '__main__':

    # y = read_excle()
    # for i in range(0, len(y)):
    #     if y[i] < 1:
    #         y[i] = 1
    # y_log = np.log2(y+0.001)
    # y_diff = difference(y_log)
    #
    # T1 = time.perf_counter()
    # px = AMPD(-y_diff.astype(int))
    # index = list()
    # for i in px:
    #     if y[i] < np.average(y)-1:
    #         index.append(i)
    # T2 = time.perf_counter()
    #
    # end_index = pickEndPressure(y, index)
    # first_index = pickFirstPressure(y, index)
    #
    # print("矿压数据的平均值为%s" % np.average(y))
    # print("AMPD函数运行了%s毫秒" % ((T2 - T1)*1000))
    #
    # plt.subplot(2, 2, 1)
    # plt.plot(range(len(y)), y)
    # plt.hlines(np.average(y), 0, 1800, colors="red", linestyles="dashed")
    #
    # plt.subplot(2, 2, 2)
    # plt.plot(range(len(y_log)), y_log)
    # plt.hlines(np.average(y_log), 0, 1800, colors="red", linestyles="dashed")
    #
    # plt.subplot(2, 2, 3)
    # plt.plot(range(len(y)), y)
    # plt.plot(range(len(y_diff)), y_diff - 20)
    # plt.scatter(index, y[index], color="red")
    # plt.scatter(index, y_diff[index]-20, color="red")
    #
    # plt.subplot(2, 2, 4)
    # for i in list(index):
    #     plt.vlines(i, 0, 50, colors="red", linestyles="dashed")
    # plt.plot(range(len(y)), y)
    # plt.scatter(end_index, y[end_index], color="green")
    # plt.scatter(first_index, y[first_index], color="orange")
    #
    # plt.show()

    import copy

    test = list()
    test1 = list(range(0, 10))
    test2 = list(range(0, 10))
    test2.reverse()

    exceedSafePressure = list()
    exceedSafePressureList = list()

    level = 5

    test = (test1 + test2) * 3
    flg = 0
    for i in range(0, len(test)):
        a = test[i]
        if test[i] >= 1:
            exceedSafePressure.append(test[i])
            flg = 1
        else:
            if flg:

                exceedSafePressureList.append(copy.deepcopy(exceedSafePressure))
                exceedSafePressure.clear()
                flg = 0
    print(test)
    print(exceedSafePressureList)

