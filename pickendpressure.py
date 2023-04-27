
# 寻找末阻点

def pickEndPressure(y, index):
    end_index_list = []
    for i in range(0, len(index)):

        step = 20

        if i != 0 and index[i] - index[i-1] <= 10:
            step = int((index[i] - index[i-1]) / 2)

        end = y[index[i] - step]
        end_index = index[i] - step

        for j in range(index[i] - step, index[i]):
            if y[j] >= end and y[j] > 10:
                end = y[j]
                end_index = j

        end_index_list.append(end_index)

    return end_index_list
