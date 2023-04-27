
# zhx的方法，找矿压曲线的包络线，缺点在于极易受异常值的影响
# 而且找到的关键点（两个周期划分点、一个初撑点、一个末阻点）不容易受控制

import json
import math
import sys
import numpy as np
from scipy.spatial import distance
import scipy.signal as singnal


# region 求取两点之间的距离
def Geodist(point1, point2):
    distanceret = distance.euclidean(point1, point2)
    return round(distanceret, 1)


# endregion


# region 包络判断函数
def get_vertical_dist(pointA, pointB, pointX):
    a = math.fabs(Geodist(pointA, pointB))
    if a == 0:
        return math.fabs(Geodist(pointA, pointX))
    b = math.fabs(Geodist(pointA, pointX))
    c = math.fabs(Geodist(pointB, pointX))
    p = (a + b + c) / 2
    S = math.sqrt(math.fabs(p * (p - a) * (p - b) * (p - c)))
    vertical_dist = S * 2 / a
    return vertical_dist


# endregion


# region 包络线规划
def DP_compress(point_list, output_point_list, Dmax):
    start_index = 0
    end_index = len(point_list) - 1
    # 定义输出点结合
    output_point_list.append(point_list[start_index])
    output_point_list.append(point_list[end_index])

    if start_index < end_index:
        index = start_index + 1
        max_vertical_dist = 0
        key_point_index = 0

        while index < end_index:
            cur_vertical_dist = get_vertical_dist(point_list[start_index], point_list[end_index], point_list[index])
            if cur_vertical_dist > max_vertical_dist:
                max_vertical_dist = cur_vertical_dist
                key_point_index = index
            index += 1

        # 递归划分
        if max_vertical_dist >= Dmax:
            DP_compress(point_list[start_index:key_point_index], output_point_list, Dmax)
            DP_compress(point_list[key_point_index:end_index], output_point_list, Dmax)


# endregion


# region 相似点去重
def SimilarityDeduplication(tempRet, criteria=1):
    tempRet = list(set(tempRet))
    tempRet = sorted(tempRet, key=lambda x: x[0])
    delList = []
    for index in range(0, len(tempRet) - 1):
        ValueRate = 0
        var = tempRet[index + 1][1]
        if tempRet[index + 1][1] >= (tempRet[index][1]) and tempRet[index][1] != 0:
            ValueRate = tempRet[index][1] / (tempRet[index + 1][1])
        if tempRet[index + 1][1] < (tempRet[index][1]) and tempRet[index + 1][1] != 0:
            ValueRate = (tempRet[index + 1][1]) / tempRet[index][1]
        if ValueRate > criteria:
            tempIndex = (index + 1) if tempRet[index + 1][1] > (tempRet[index][1]) else index
            delList.append(tempIndex)
    delList = list(set(delList))
    dicRet = {}
    for key in range(len(tempRet)):
        dicRet[key] = tempRet[key]
    [dicRet.pop(i) for i in delList]
    ret = list(dicRet.values())
    return ret


# endregion


# region 周期的划分
def SimilarityCycelDeduplication(tempRet, num=10):
    ret = tempRet.copy()
    listRet = []
    ret = sorted(ret, key=lambda x: x[1])

    avrage = (ret[-1][1] - ret[0][1]) / 2

    ret = sorted(ret, key=lambda x: x[0])
    for item in range(len(ret) - 1):
        if ret[item][1] < avrage:
            minDistance = sys.maxsize
            minDisIndx = 0
            for index in range(item + 1, len(ret)):
                if ret[index][1] < avrage:
                    val = abs(ret[item][0] - ret[index][0])
                    if val < minDistance:
                        minDistance = val
                        minDisIndx = ret[index][0]
            if minDistance != sys.maxsize:
                listRet.append((ret[item][0], minDisIndx, minDistance))
    # 震荡间距
    avgDistance = num

    temp = []
    for item in range(len(listRet)):
        if listRet[item][2] < avgDistance:
            for index in range(len(tempRet)):
                if tempRet[index][0] == listRet[item][0]:
                    temp.append(index)
    temp = list(set(temp))
    dicRet = {}
    for key in range(len(tempRet)):
        dicRet[key] = tempRet[key]
    [dicRet.pop(i) for i in temp]
    return list(dicRet.values())


# endregion


# region 结构化数据输出
def dataStructionRet(finshRet):
    retList = finshRet.copy()
    # 索引列表
    retIndex = []
    # 数值列表
    retValue = []
    for item in range(len(retList)):
        retIndex.append(retList[item][0])
        retValue.append(retList[item][1])
    retIndex1 = singnal.argrelextrema(np.array(retValue), np.less)
    lessTemp = list(retIndex1[0])
    lesser = []
    for index in range(0, len(lessTemp)):
        if retValue[lessTemp[index]] > np.median(np.array(retValue)) * 0.5:
            lesser.append(index)
    dic = {}
    for index in range(len(lessTemp)):
        dic[index] = lessTemp[index]
    [dic.pop(i) for i in list(set(lesser))]
    ret = list(dic.values())

    # 结构化数据输出。此处输出完整的周期，非完整周期没法进行判断
    dicLastRet = {}
    for item in range(0, len(ret) - 1):
        dataTemp = []
        beforCycleMinId = retIndex[ret[item]]
        nextCycleMinId = retIndex[ret[item + 1]]
        a, b = maxRevers(beforCycleMinId, nextCycleMinId, retValue, retIndex)

        dataTemp.append(beforCycleMinId)
        dataTemp.append(a)
        dataTemp.append(b)
        dataTemp.append(nextCycleMinId)
        dicLastRet[item + 1] = dataTemp
    return retValue, retIndex, ret, dicLastRet


# endregion


def maxRevers(indexStart, indexEnd, retValue, retIndex):
    index = []
    index1 = []
    tempBefor = []
    tempNext = []
    intialData = 0
    finishData = 0
    for i in range(len(retIndex)):
        if indexStart <= retIndex[i] <= (indexEnd + indexStart) / 2:
            index.append(i)
            tempBefor.append(retIndex[i])
    for i in range(len(retIndex)):
        if (indexEnd + indexStart) / 2 <= retIndex[i] <= indexEnd:
            index1.append(i)
            tempNext.append(retIndex[i])
    ret = [retValue[x] for x in index]
    intialData = tempBefor[np.argmax(ret)]
    ret1 = [retValue[x] for x in index1]
    finishData = tempNext[np.argmax(ret1)]
    return intialData, finishData


if __name__ == '__main__':
    fileArg = sys.argv[:]
    if len(fileArg) <= 1:
        print("缺少数据文件参数")
    try:
        # 读取.net生成的计算数据文件
        # 加载json数据
        # 进行解析
        # 进行计算
        # 数据结果json化返回
        with open(fileArg[1], 'r') as f:
            # with open(r"D:\pythonProject\DataDeal\test.json", 'r') as f:
            data = json.load(f)
            loadData = data["PressureValue"]
        if len(loadData) <= 100:
            print("数据量不足一个周期")
        inputData = []
        loadData = list(loadData)
        for i in range(0, len(loadData)):
            inputData.append((i, loadData[i]))
        tempOut = []
        ret = []
        DP_compress(inputData, tempOut, 10)
        ret = SimilarityDeduplication(tempOut)
        ret = SimilarityCycelDeduplication(ret)
        a, b, c, d = dataStructionRet(ret)
        jsonStr = json.dumps(d)
        print(jsonStr)
    except:
        print("计算失败")
