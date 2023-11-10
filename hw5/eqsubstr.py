# Write a function, which when iven one string (s) and two characters
# (c1 and c2), computes all pairings of contiguous ranges of c1s
# and c2s that have the same length.  Your function should return
# a set of three-tuples.  Each element of the set should be
# (c1 start index, c2 start index, length)
#
# Note that s may contain other characters besides c1 and c2.
# Example:
#  s = abcabbaacabaabbbb
#      01234567890111111  <- indices for ease of looking
#                1123456
#  c1 = a
#  c2 = b
#  Observe that there are the following contiguous ranges of 'a's (c1)
#  Length 1: starting at 0, 3, 9
#  Length 2: starting at 6, 11
#  And the following contiguous ranges of 'b's (c2)
#  Length 1: starting at 1, 10
#  Length 2: starting at 4
#  Length 4: starting at 13
#  So the answer would be
#  { (0, 1, 1), (0, 10, 1), (3, 1, 1), (3, 10, 1), (9, 1, 1), (9, 10, 1),
#    (6, 4, 2), (11, 4, 2)}
#  Note that the length 4 range of 'b's does not appear as there are no
#  Length 4 runs of 'a's.
import time
import random
import matplotlib.pyplot as plt
import pandas as pd
def matching_length_sub_strs(s, c1, c2):
    # WRITE ME
    
    c1_dict = {}
    c2_dict = {}
    ans = set()
    
    # first find the index and the contiguous ranges of c1 and c2
    count1 = 0
    count2 = 0
    for i in range(len(s)):
        if s[i] == c1:
            count1 = count1 + 1
        if s[i] != c1 or i == len(s)-1:
            index1 = i - count1
            if i == len(s)-1:
                index1 = i - count1 + 1
            if count1 != 0:
                if count1 in c1_dict:
                    c1_dict[count1].append(index1)
                else:
                    c1_dict[count1] = [index1]
                count1 = 0
                
        if s[i] == c2:
            count2 = count2 + 1
        if s[i] != c2 or i == len(s)-1:
            index2 = i - count2
            if i == len(s)-1:
                index2 = i - count2 + 1
            if count2 != 0:
                if count2 in c2_dict:
                    c2_dict[count2].append(index2)
                else:
                    c2_dict[count2] = [index2]
                count2 = 0

    for key in c1_dict:
        if key in c2_dict:
            for c1_value in c1_dict[key]:
                for c2_value in c2_dict[key]:
                    tuple = (c1_value, c2_value, int(key))
                    ans.add(tuple)

    return ans


# Makes a random string of length n
# The string is mostly comprised of 'a' and 'b'
# So you should use c1='a' and c2='b' when
# you use this with matching_length_sub_strs
def rndstr(n):
    def rndchr():
        x=random.randrange(7)
        if x==0:
            return chr(random.randrange(26)+ord('A'))
        if x<=3:
            return 'a'
        return 'b'
    ans=[rndchr() for i in range(n)]
    return "".join(ans)

# write a function 
def getSize(n):
    size = [n]
    while n < 16384:
        n = n*2
        size.append(n)
    return size

# write a function to generate the best case
# the best case should only have (a*b*) U (b*a*)
def getBest(n):
    ans = ''
    pattern_choice = random.choice([1, 2])  
    length = n
    if pattern_choice == 1:
        a_count = random.randint(0, length)
        b_count = length - a_count
        sequence = ['a'] * a_count + ['b'] * b_count
        ans = "".join(sequence)    
    else:
        b_count = random.randint(0, length)
        a_count = length - b_count
        sequence = ['b'] * b_count + ['a'] * a_count
        ans = ''.join(sequence)
    return ans

# write a function to generate the best case
def getWorst(n):
    ans = ""
    for i in range(int(n/2)):
        ans += "ab"
    return ans

def getString(sizeArr):
    best = []
    worst = []
    randomS = []
    for i in range(len(sizeArr)):
        best.append(getBest(sizeArr[i]))
        worst.append(getWorst(sizeArr[i]))
        randomS.append(rndstr(sizeArr[i]))
    return [best, worst, randomS]

def getTime(strings):
    timeBest = []
    timeWorst =[]
    timeRandom = []
    
    for i in range(len(strings[0])):
        timeBeforeBest = time.time()
        matching_length_sub_strs(strings[0][i], "a", "b")
        timeBest.append(time.time() - timeBeforeBest)
        
        timeBeforeWorst = time.time()
        matching_length_sub_strs(strings[1][i], "a", "b")
        timeWorst.append(time.time() - timeBeforeWorst)
        
        timeBeforeRandom = time.time()
        matching_length_sub_strs(strings[2][i], "a", "b")
        timeRandom.append(time.time() - timeBeforeRandom)
    
    return [timeBest, timeWorst, timeRandom]

def main():
    sizeArr = getSize(512)
    strings1 = getString(sizeArr)
    time1 = getTime(strings1)
    strings2 = getString(sizeArr)
    time2 = getTime(strings2)
    strings3 = getString(sizeArr)
    time3 = getTime(strings3)
    time = []
    rowname = []
    
    # calculate the average runtime
    for i in range(3):
        tmp = []
        for j in range(len(sizeArr)):
            tmp.append((time1[i][j] + time2[i][j] + time3[i][j]) / 3)
        time.append(tmp)

    for i in range(len(sizeArr)):
        rowname.append(str(sizeArr[i]))
        print(sizeArr[i], ",",
              time[0][i], ",",
              time[1][i], ",",
              time[2][i], "\n")
    
    # The following part are comment for submitting
    
    # Save plot
    # plt.figure(figsize=(8, 6))

    # plt.plot(sizeArr, time[0], label='Best Case', color='blue')
    # plt.plot(sizeArr, time[1], label='Worst Case', color='green')
    # plt.plot(sizeArr, time[2], label='Random Input', color='red')
    # plt.xlabel('Input Size')
    # plt.ylabel('Runtime (second)')
    # plt.title('Matching Length Substrings')
    # plt.legend()

    # plt.savefig('q3.png')
    
    # #import packages

    # fig, ax =plt.subplots(1, 1)

    # table = pd.DataFrame()
    # table['Best Case(s)'] = time[0]
    # table['Worst Case(s)'] = time[1]
    # table['Random Input(s)'] = time[2]
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
    # plt.savefig('q3_table.png')
    
    return 0

if __name__ == "__main__":
    main()