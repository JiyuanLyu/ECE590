import time

def readVault():
    return 0

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

A = [[0, 4, 1, 3, 11],
     [8, 2, 4, 5, 6],
     [1, 7, 3, 9, 0],
     [0, 12, 1, 2, 0]]

path, coin = findPath(A)
print(path)
print(coin)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vault.py <filename>")
        sys.exit(1)