from functools import cache
import sys
import time

sys.setrecursionlimit(20000)

def findPathNCache(A, x, y, path):
    nrow = len(A)
    ncol = len(A[0])
    
    if x == nrow - 1 and y == ncol - 1:
        return path[::-1], A[x][y]
    elif x == nrow - 1:
        path += "W"
        next_path, next_val = findPathNCache(A, x, y + 1, path)
        return next_path, A[x][y] + next_val
    elif y == ncol - 1:
        path += "N"
        next_path, next_val = findPathNCache(A, x + 1, y, path)
        return next_path, A[x][y] + next_val
    
    # if go south(N)
    pN, cN = findPathNCache(A, x + 1, y, path)
    # if go east(W)
    pW, cW = findPathNCache(A, x, y + 1, path)
    
    if cN > cW: 
        pN += "N"
        return pN, A[x][y] + cN
    else:
        pW += "W"
        return pW, A[x][y] + cW


def main():
    input_path = sys.argv[1]

    file = open(input_path, 'r').readlines()
    inputs = [list(map(int, line.strip().split(','))) for line in file]
    inputs = tuple(tuple(row) for row in inputs)
    #inputs = tuple(inputs) 
    timeBefore = time.perf_counter_ns()
    #coins= recursion(inputs, 0, 0)
    path, coins = findPathNCache(inputs, 0, 0, "")
    timeAfter = time.perf_counter_ns() - timeBefore
    
    print(path)
    print(coins)
    print(timeAfter)

if __name__ == "__main__":
    main()        
