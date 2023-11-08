# removes duplicates from data.
# This function keeps the last occurence of each element
# and preserves order.
# So rmdup([1,2,3,2,1,4,2]) should return [3,1,4,2]

# Import necessary package
import time
import random
import matplotlib.pyplot as plt
import pandas as pd

# write the function removes duplicates
def rmdup(data):
    # Write me
    unique = {}
    last_occur = []

    # reverse the data array
    for element in reversed(data):#range(len(data)-1, -1, -1):#reversed(data):
        # if this element not record yet, record
        if element not in unique:
            last_occur.append(element)
            unique[element] = True

    # return the reverse of the recording array
    last_occur.reverse()
    return last_occur

# write a function to generte different data size
def getSize(size):
    sizeArr = []
    for i in range(11):
        sizeArr.append(size)
        size = size * 2
    return sizeArr

# write a function to get data
def getData(size):
    dataMany = []
    dataModerate = []
    dataRare = []

    for i in range(size):
        dataMany.append(random.randrange(0, size/2048))
        dataModerate.append(random.randrange(0, size/16))
        dataRare.append(random.randrange(0, size/4))
    return [dataMany, dataModerate, dataRare]

# write a function to get time
def getTime(sizeArr):
    timeMany = []
    timeModerate = []
    timeRare = []
    for i in range(len(sizeArr)):
        dataMany = getData(sizeArr[i])[0]
        dataModerate = getData(sizeArr[i])[1]
        dataRare = getData(sizeArr[i])[2]

        timeBeforeM = time.time()
        rmdup(dataMany)
        timeAfterM = time.time()
        timeMany.append(timeAfterM - timeBeforeM)

        timeBeforeMd = time.time()
        rmdup(dataModerate)
        timeAfterMd = time.time()
        timeModerate.append(timeAfterMd - timeBeforeMd)

        timeBeforeR = time.time()
        rmdup(dataRare)
        timeAfterR = time.time()
        timeRare.append(timeAfterR - timeBeforeR)

    return [timeMany, timeModerate, timeRare]

def main():
    sizeArr = getSize(4096)
    timeArr1 = getTime(sizeArr)
    timeArr2 = getTime(sizeArr)
    timeArr3 = getTime(sizeArr)
    timeArr = []
    rowname = []
    
    # calculate the average runtime
    for i in range(3):
        tmp = []
        for j in range(len(sizeArr)):
            tmp.append((timeArr1[i][j] + timeArr2[i][j] + timeArr3[i][j]) / 3)
        timeArr.append(tmp)
        
    # print the runtime
    for i in range(len(sizeArr)):
        rowname.append(str(sizeArr[i]))
        print(sizeArr[i], ",",
              timeArr[0][i], ",",
              timeArr[1][i], ",",
              timeArr[2][i], "\n")
        
    # The following part are comment for submitting
    # # Save plot
    # plt.figure(figsize=(8, 6))

    # plt.plot(sizeArr, timeArr[0], label='Many Duplicates', color='blue')
    # plt.plot(sizeArr, timeArr[1], label='Moderate Duplication', color='green')
    # plt.plot(sizeArr, timeArr[2], label='Rare Duplication', color='red')
    # plt.xlabel('Data Size')
    # plt.ylabel('Runtime')
    # plt.title('Remove Duplicates Runtime')
    # plt.legend()

    # plt.savefig('q1.png')
    
    # fig, ax =plt.subplots(1, 1)

    # table = pd.DataFrame()
    # table['Many Duplicates'] = timeArr[0]
    # table['Moderate Duplication'] = timeArr[1]
    # table['Rare Duplication'] = timeArr[2]
    # table.index = rowname # type: ignore
        
    # ax.axis('tight')
    # ax.axis('off')

    # #plotting data
    # table = ax.table(cellText = table.values,
    #         colLabels = table.columns,
    #         rowLabels = sizeArr,
    #         loc="center")
    # table.set_fontsize(14)
    # table.scale(1,2)
    # plt.savefig('q1_table.png')
    return 0


if __name__ == "__main__":
    main()