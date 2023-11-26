import sys
import time
import random
import matplotlib.pyplot as plt
import pandas as pd
from functools import cache

sys.setrecursionlimit(50000)

def readVault(filename):
    file = open(filename, 'r').readlines()
    matrix = [list(map(int, line.strip().split(','))) for line in file]
    matrix = tuple(tuple(row) for row in matrix)
    return matrix

@cache
def findPath(A, x, y, path):
    nrow = len(A)
    ncol = len(A[0])
    
    if x == nrow - 1 and y == ncol - 1:
        return path[::-1], A[x][y]
    elif x == nrow - 1:
        next_path, next_val = findPath(A, x, y + 1, path + "W")
        return next_path, A[x][y] + next_val
    elif y == ncol - 1:
        next_path, next_val = findPath(A, x + 1, y, path + "N")
        return next_path, A[x][y] + next_val
    
    # if go south(N)
    pN, cN = findPath(A, x + 1, y, path + "N")
    # if go east(W)
    pW, cW = findPath(A, x, y + 1, path + "W")
    
    if cN > cW: 
        return pN, A[x][y] + cN
    else:
        return pW, A[x][y] + cW


# A = [[0, 4, 1, 3, 11],
#      [8, 2, 4, 5, 6],
#      [1, 7, 3, 9, 0],
#      [0, 12, 1, 2, 0]]


# timeB = time.perf_counter_ns()
# p = ""
# path, coin = findPath(A, 0, 0, p)
# timeA = time.perf_counter_ns() - timeB
# print(path)
# print(coin)
# print(timeA)


# write a function to get an array of size N
def getN(x, y):
    tmp = x
    ans = [tmp]
    
    while tmp < y:
        tmp = tmp * 2
        ans.append(tmp)
    
    return ans

# get Matrix
def getMatrix(row, column):
    ans = []
    for i in range(int(row)):
        temp = []
        for j in range(int(column)):
            temp.append(random.randrange(0, 1000))
        ans.append(temp)
    return tuple(map(tuple,ans))

# get the runtime array
def getTime(arrN):
    timeR = []
    timeS = []
    timeC = []
    for i in range(len(arrN)):
        # Many rows by few columns
        a_R = getMatrix(arrN[i]*4, arrN[i])
        timeBeforeR = time.perf_counter_ns()
        findPath(a_R, 0, 0, "")
        timeR.append(time.perf_counter_ns() - timeBeforeR)
        
        # Square
        a_S = getMatrix(arrN[i], arrN[i])
        timeBeforeS = time.perf_counter_ns()
        findPath(a_S, 0, 0, "")
        timeS.append(time.perf_counter_ns() - timeBeforeS)
        
        # Many rows by few columns
        a_C = getMatrix(arrN[i]/4, arrN[i])
        timeBeforeC = time.perf_counter_ns()
        findPath(a_C, 0, 0, "")
        timeC.append(time.perf_counter_ns() - timeBeforeC)
        
    return [timeR, timeS, timeC]

def getExpResult():
    arrN = getN(4, 256)
    time1 = getTime(arrN)
    time2 = getTime(arrN)
    time3 = getTime(arrN)
    time = []
    rowname = []
# calculate the average runtime
    for i in range(3):
        tmp = []
        for j in range(len(arrN)):
            tmp.append((time1[i][j] + time2[i][j] + time3[i][j]) / 3)
        time.append(tmp)
        
    # print the runtime
    for i in range(len(arrN)):
        rowname.append(str(arrN[i]))
        print(arrN[i], ",",
              time[0][i], ",",
              time[1][i], ",",
              time[2][i], "\n")
    
    # save plot
    plt.figure(figsize=(8, 6))

    plt.plot(arrN, time[0], label='Many Rows by Few Columns', color='blue')
    plt.plot(arrN, time[1], label='Sqaure', color='green')
    plt.plot(arrN, time[2], label='Few Rows by Many Columns', color='red')
    plt.xlabel('N')
    plt.ylabel('Runtime (nanoseconds)')
    plt.title('Vault.py Runtime')
    plt.legend()

    plt.savefig('q2.png')

    fig, ax =plt.subplots(1, 1)

    table = pd.DataFrame()
    table['Many Rows by Few Columns (s)'] = time[0]
    table['Sqaure (s)'] = time[1]
    table['Few Rows by Many Columns (s)'] = time[2]
    table.index = rowname # type: ignore
        
    ax.axis('tight')
    ax.axis('off')

    #plotting data
    table = ax.table(cellText = table.values,
            colLabels = table.columns,
            rowLabels = arrN,
            loc="center")
    table.set_fontsize(14)
    table.scale(1,2)
    plt.savefig('q1_table.png')
    return 0

def main():
    filename = sys.argv[1]
    matrix = readVault(filename)
    timeB = time.perf_counter_ns()
    p = ""
    path, coin= findPath(matrix, 0, 0, p)
    timeA = time.perf_counter_ns() - timeB
    print(path)
    print(coin)
    print(timeA)
    # getExpResult()
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input arguments number is wrong!")
        sys.exit(1)
    main()