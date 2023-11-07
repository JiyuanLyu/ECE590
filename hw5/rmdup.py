# removes duplicates from data.
# This function keeps the last occurence of each element
# and preserves order.
# So rmdup([1,2,3,2,1,4,2]) should return [3,1,4,2]

# Import necessary package
import time
import random

# write the function removes duplicates
def rmdup(data):
    # Write me
    last_occur = []

    # reverse the data array
    for element in reversed(data):
        # if this element not record yet, record
        if element not in last_occur:
            last_occur.append(element)

    # return the reverse of the recording array
    last_occur.reverse()
    return last_occur

# test the function
#data = [1,2,3,2,1,4,2]
#result = rmdup(data)
#print(result)

# write a function to generate different data size
def getSize(size):
    sizeArr = []
    while size < 4194304:
        sizeArr.append(size)
        size *= 2
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

# write a function to generate data
def getTime(sizeArr):
    timeMany = []
    timeModerate = []
    timeRare = []
    for i in range(len(sizeArr)):
        dataMany = getData(sizeArr[i])[0]
        timeMany.append(rmdup(dataMany).time())
        dataModerate = getData(sizeArr[i])[1]
        timeModerate.append(rmdup(dataModerate).time())
        dataRare = getData(sizeArr[i])[2]
        timeRare.append(rmdup(dataRare).time())

    return [timeMany, timeModerate, timeRare]

def main():
    sizeArr = getSize(4096)
    timeArr = getTime(sizeArr)
    for i in range(len(sizeArr)):
        for j in range(len(timeArr)):
            print(sizeArr[i], ",",
                  timeArr[0][j], ",",
                  timeArr[1][j], ",",
                  timeArr[2][j], "\n")
    return 0


if __name__ == "__main__":
    main()