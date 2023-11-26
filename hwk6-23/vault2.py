from functools import cache
import sys

sys.setrecursionlimit(20000)

@cache
def recursion(record, x, y):
    c = len(record[0]) - 1
    r = len(record) - 1

    if(x == r and y == c):
        return record[x][y]
    if(x == r): 
        return record[x][y] + recursion(record, x, y + 1)
    if(y == c): 
        return record[x][y] + recursion(record,x+1,y)
    return record[x][y]+max(recursion(record,x+1,y),recursion(record, x, y + 1))



def main():
    input_path = sys.argv[1]

    file = open(input_path, 'r').readlines()
    inputs = [list(map(int, line.strip().split(','))) for line in file]
    inputs = tuple(tuple(row) for row in inputs)
    #inputs = tuple(inputs) 
  
    coins= recursion(inputs, 0, 0)
    print(coins)

if __name__ == "__main__":
    main()        
