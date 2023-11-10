# This function takes 2 matricies (as lists of lists)
# and performs matrix multiplication on them.
# Note: you may not use any matrix multiplication libraries.
# You need to do the multiplication yourself.
# For example, if you have
#     a=[[1,2,3],
#        [4,5,6],
#        [7,8,9],
#        [4,0,7]]
#     b=[[1,2],
#        [3,4],
#        [5,6]]
#  Then a has 4 rows and 3 columns.
#  b has 3 rows and 2 columns.
#  Multiplying a * b results in a 4 row, 2 column matrix:
#  [[22, 28],
#   [49, 64],
#   [76, 100],
#   [39, 50]]

import random
import time
import matplotlib.pyplot as plt
import pandas as pd


def matrix_mul(a,b):
    # Write me

    # let A * B = C
    c = []
    # For all rows in a
    for i in range(len(a)):
        # multiply with the columns in b
        row = []
        for j in range(len(b[0])):
            element = 0
            # add all the multiplications
            for k in range(len(b)):
                element += a[i][k] * b[k][j]
            # append this element to the row
            row.append(element)
        # append this row to the c matrix
        c.append(row)

    return c 

# write a function to get an array of N
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
        b_R = getMatrix(arrN[i], arrN[i]/4)
        timeBeforeR = time.time()
        matrix_mul(a_R, b_R)
        timeR.append(time.time() - timeBeforeR)
        
        # Square
        a_S = getMatrix(arrN[i], arrN[i])
        b_S = getMatrix(arrN[i], arrN[i])
        timeBeforeS = time.time()
        matrix_mul(a_S, b_S)
        timeS.append(time.time() - timeBeforeS)
        
        # Many rows by few columns
        a_C = getMatrix(arrN[i]/4, arrN[i])
        b_C = getMatrix(arrN[i], arrN[i]*4)
        timeBeforeC = time.time()
        matrix_mul(a_C, b_C)
        timeC.append(time.time() - timeBeforeC)
        
    return [timeR, timeS, timeC]

def main():
    arrN = getN(4, 512)
    print(arrN)
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
    
    # The following part are comment for submitting
    # # save plot
    # plt.figure(figsize=(8, 6))

    # plt.plot(arrN, time[0], label='Many Rows by Few Columns', color='blue')
    # plt.plot(arrN, time[1], label='Sqaure', color='green')
    # plt.plot(arrN, time[2], label='Few Rows by Many Columns', color='red')
    # plt.xlabel('N')
    # plt.ylabel('Runtime (seconds)')
    # plt.title('Matrix Multiplication Runtime')
    # plt.legend()

    # plt.savefig('q2.png')

    # fig, ax =plt.subplots(1, 1)

    # table = pd.DataFrame()
    # table['Many Rows by Few Columns (s)'] = time[0]
    # table['Sqaure (s)'] = time[1]
    # table['Few Rows by Many Columns (s)'] = time[2]
    # table.index = rowname # type: ignore
        
    # ax.axis('tight')
    # ax.axis('off')

    # #plotting data
    # table = ax.table(cellText = table.values,
    #         colLabels = table.columns,
    #         rowLabels = arrN,
    #         loc="center")
    # table.set_fontsize(14)
    # table.scale(1,2)
    # plt.savefig('q2_table.png')
    return 0

if __name__ == "__main__":
    main()