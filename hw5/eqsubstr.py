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
import random
def matching_length_sub_strs(s, c1, c2):
    # WRITE ME
    
    a_conti = {}
    b_conti = {}
    ans = set()
    # first find the index and the contiguous ranges of c1 and c2
    for i in range(len(s)):
        if s[i] == c1:
            index = i
            count = 1
            for j in range(i+1,len(s)):
                if s[j] == c1:
                    count += 1
            a_conti[count] = index
        if s[i] == c2:
            index = i
            count = 1
            for j in range(i+1,len(s)):
                if s[j] == c2:
                    count += 1
            b_conti[count] = index
    
    for a_key in range(a_conti.keys()):
        for b_key in range(b_conti.keys()):
            if a_key == b_key:
                for a in a_conti[a_key]:
                    for b in b_conti[a_key]:
                        ans_row = [a, b, a_key]
                        ans.append(ans_row)

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

    
s = "abcabbaacabaabbbb"
c1 = "a"
c2 = "b"
ans = matching_length_sub_strs(s, c1, c2)
print(ans)