import sys
import time
import random
import matplotlib.pyplot as plt
import pandas as pd

def readVault(filename):
    matrix = []

    with open(filename, 'r') as file:
        for line in file:
            row = [int(num) for num in line.strip().split(',')]
            matrix.append(row)

    return matrix

def findPath(A):
    path = ""
    coin  = 0
    nrow = len(A)
    ncol = len(A[0])
    
    coin = coin + A[0][0]
    currR = 0
    currC = 0
    while currR <= nrow-1 and currC <= ncol-1:
        if currR == nrow-1 and currC == ncol-1:
            coin = coin + A[nrow-1][ncol-1]
            break
        path, coin, currR, currC = findMaxCoin(A, path, coin, currR, currC)
    return path[::-1], coin


# this function find the max coin path from the end to the start
def findMaxCoin(A, path, coin, currR, currC):
    nn = 0
    nw = 0
    ww = 0
    wn = 0
    
    nrow = len(A)
    ncol = len(A[0])
            
    # check if it can go back to south (the dragon go north)
    n = 0
    if currR + 1 < nrow:
        n = A[currR+1][currC]
        # check if it can keep going back to south
        if currR + 2 < nrow:
            nn = n + A[currR+2][currC]
        else:
            nn = n
        # check if it can go back to east next
        if currC + 1 < ncol:
            nw = n + A[currR+1][currC+1]
        else:
            nw = n
        
    # check if it can go back to east
    w = 0
    if currC + 1 < ncol:
        w = A[currR][currC+1]
        # check if keep going east
        if currC + 2 < ncol:
            ww = w + A[currR][currC+2]
        else:
            ww = w
        # check if go back to south
        if currR + 1 < nrow:
            wn = w + A[currR+1][currC+1]
        else:
            wn = w
                    
    my_arr = [nn, nw, ww, wn]
    mostIndex = my_arr.index(max(my_arr))
    if currR == nrow - 2 and currC == ncol - 1:
        coin += n
        path += "N"
        nextR = currR + 1
        nextC = currC
    elif currR == nrow - 1 and currC == ncol - 2:
        coin += w
        path += "W"
        nextR = currR
        nextC = currC + 1
    else:
        if mostIndex < 2:
            coin += n
            path += "N"
            nextR = currR + 1
            nextC = currC
        else:
            coin += w
            path += "W"
            nextR = currR
            nextC = currC + 1
    return path, coin, nextR, nextC

# A = [[0, 4, 1, 3, 11],
#      [8, 2, 4, 5, 6],
#      [1, 7, 3, 9, 0],
#      [0, 12, 1, 2, 0]]

# path, coin = findPath(A)
# print(path)
# print(coin)


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
    return ans

# get the runtime array
def getTime(arrN):
    timeR = []
    timeS = []
    timeC = []
    for i in range(len(arrN)):
        # Many rows by few columns
        a_R = getMatrix(arrN[i]*4, arrN[i])
        timeBeforeR = time.time()
        findPath(a_R)
        timeR.append(time.time() - timeBeforeR)
        
        # Square
        a_S = getMatrix(arrN[i], arrN[i])
        timeBeforeS = time.time()
        findPath(a_S)
        timeS.append(time.time() - timeBeforeS)
        
        # Many rows by few columns
        a_C = getMatrix(arrN[i]/4, arrN[i])
        timeBeforeC = time.time()
        findPath(a_C)
        timeC.append(time.time() - timeBeforeC)
        
    return [timeR, timeS, timeC]

def getExpResult():
    arrN = getN(4, 512)
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
    plt.ylabel('Runtime (seconds)')
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
    # filename = sys.argv[1]
    # matrix = readVault(filename)
    # path, coin= findPath(matrix)
    # print(path)
    # print(coin)
    getExpResult()
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input arguments number is wrong!")
        sys.exit(1)
    main()