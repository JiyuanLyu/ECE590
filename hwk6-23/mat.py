import sys
import time
import random
import matplotlib.pyplot as plt
import pandas as pd
from functools import cache
sys.setrecursionlimit(50000)

# Function to read dimensions from a file and generate matrices
def readMatrix(filename):
    matrices = []
    with open(filename, 'r') as file:
        for line in file:
            name, rows, columns = line.strip().split(',')
            matrices.append((name, int(rows), int(columns)))
    return tuple(matrices)

@cache
def findOpe(matrices, i, j):
    if i == j:
        return 0, matrices[i][0]

    minOpe = sys.maxsize
    order = None

    for k in range(i, j):
        ops_left, order_left = findOpe(matrices, i, k)
        ops_right, order_right = findOpe(matrices, k + 1, j)
        currOpe = ops_left + ops_right + matrices[i][1] * matrices[k][2] * matrices[j][2]

        if currOpe < minOpe:
            minOpe = currOpe
            order = (order_left, order_right)

    return minOpe, order


def findOpeNCache(matrices, i, j):
    if i == j:
        return 0, matrices[i][0]

    minOpe = sys.maxsize
    order = None

    for k in range(i, j):
        ops_left, order_left = findOpeNCache(matrices, i, k)
        ops_right, order_right = findOpeNCache(matrices, k + 1, j)
        currOpe = ops_left + ops_right + matrices[i][1] * matrices[k][2] * matrices[j][2]

        if currOpe < minOpe:
            minOpe = currOpe
            order = (order_left, order_right)

    return minOpe, order

# write a function to get an array of size N
def getN(x, y):
    tmp = x
    ans = [tmp]
    
    while tmp < y:
        tmp = tmp * 2
        ans.append(tmp)
    
    return ans

# write a function to get an array of size N
def getMatrices(n):
    matrices = []
    for i in range(n):
        name = chr(ord('A') + i)  # Generate matrix names A, B, C, ...
        rows = random.randint(1, 100)  # Random number of rows (1 to 10)
        cols = random.randint(1, 100)  # Random number of columns (1 to 10)
        matrices.append((name, rows, cols))
    return tuple(matrices)

def getTime(arrN):
    timeS = []
    for i in range(len(arrN)):
        matrices = getMatrices(arrN[i])
        timeBeforeS = time.perf_counter_ns()
        findOpe(matrices, 0, len(matrices) - 1)
        timeS.append(time.perf_counter_ns() - timeBeforeS)
    return timeS

def getTimeNCache(arrN):
    timeS = []
    for i in range(len(arrN)):
        matrices = getMatrices(arrN[i])
        timeBeforeS = time.perf_counter_ns()
        findOpeNCache(matrices, 0, len(matrices) - 1)
        timeS.append(time.perf_counter_ns() - timeBeforeS)
    return timeS 

def getExpResult():
    arrN = getN(1, 512)
    nocache = []
    for i in arrN:
        nocache.append(0)
    noN = [1, 2, 4, 8, 16]
    nocache = getTimeNCache(noN)
    for i in range(len(arrN) - 5):
        nocache.append(0)
        
        
    time = getTime(arrN)
    
    # save plot
    plt.figure(figsize=(8, 6))

    plt.plot(arrN, time, label='Runtime (with @cache)', color='green')
    plt.plot(arrN, nocache, label='Runtime (without @cache)', color='red', linestyle="dashed")
    plt.xlabel('N')
    plt.ylabel('Runtime (nanoseconds)')
    plt.title('mat.py Runtime')
    plt.legend()

    plt.savefig('q2.png')

    fig, ax =plt.subplots(1, 1)

    table = pd.DataFrame()
    table['With Cache (nanoseconds)'] = time
    table['Without Cache (nanoseconds)'] = nocache
    ax.axis('tight')
    ax.axis('off')

    #plotting data
    table = ax.table(cellText = table.values,
            colLabels = table.columns,
            rowLabels = arrN,
            loc="center")
    table.set_fontsize(14)
    table.scale(1,2)
    plt.savefig('q2_table.png')
    return 0

def main():
    # filename = sys.argv[1]
    # matrices = readMatrix(filename)
    # timeB = time.perf_counter_ns()
    # minOpe, order = findOpe(matrices, 0, len(matrices) - 1)
    # timeA = time.perf_counter_ns() - timeB
    # print(order)
    # print(minOpe)
    # print(timeA)
    getExpResult()
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input arguments number is wrong!")
        sys.exit(1)
    main()