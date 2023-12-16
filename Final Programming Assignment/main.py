from cgi import test
import copy
from numpy import true_divide
from regex import *
from state import * 
from nfa import *
from dfa import *
from queue import deque # type: ignore

# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    dfa = DFA()
    dfa.alphabet = nfa.alphabet
    stateLen = 0
    dfa.states.append(State(stateLen))
    
    tempSet = {}
    for i in range(len(nfa.states)):
        setState = set([nfa.states[i]])
        while(setState != nfa.epsilonClosureDFA(setState)):
            setState = nfa.epsilonClosureDFA(setState)
        myset = []
        myset.append(i)
        for j in setState:
            myset.append(j.id)
        tempSet[i] = set(myset)
    nfa_info = [tempSet[0]]
    
    for state in tempSet[0]:
        if nfa.is_accepting[state] == True:
            dfa.is_accepting[stateLen] = True
            break
        else: 
            dfa.is_accepting[stateLen] = False

    stateLen += 1
    
    curr = 0

    while(True):
        for c in dfa.alphabet:
            s = set()
            for i in nfa_info[curr]:
                if c in nfa.states[i].transition:
                    for j in nfa.states[i].transition[c]:
                        s.add(j.id)
                        
            if s == set():
                continue
            
            ans=[]
            for i in s:
                ans.append(i)
                for j in tempSet[i]:
                    ans.append(j)
            s = set(ans)
            
            n = 0
            for i in range(len(nfa_info)):
                if s==nfa_info[i]:
                    break
                n += 1
            
            if n<stateLen:
                dfa.addTransition(dfa.states[curr], dfa.states[n], c)
            else:
                dfa.states.append(State(stateLen))
                nfa_info.append(s)
                
                for it in s:
                    if nfa.is_accepting[it]==True:
                        dfa.is_accepting[stateLen] = True
                        break
                    dfa.is_accepting[stateLen] = False
                
                stateLen += 1
                dfa.addTransition(dfa.states[curr], dfa.states[n], c)
        curr += 1
        if curr >= stateLen:
            break
        
    return dfa

# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    nfa.states = copy.deepcopy(dfa.states)
    nfa.is_accepting= copy.deepcopy(dfa.is_accepting)
    nfa.alphabet = copy.deepcopy(dfa.alphabet)
    return nfa

# here I write a union function to help test the equivalent
# the function will take two nfa and return a union nfa
def union_nfas(nfa1, nfa2):
    union_nfa = NFA()
    union_nfa = copy.deepcopy(nfa1)
    unionLength = len(union_nfa.states)
    
    union_nfa.addStatesFrom(nfa2)
    union_nfa.addTransition(union_nfa.states[0],union_nfa.states[unionLength])
    
    for i in nfa2.alphabet:
        if i not in union_nfa.alphabet:
            union_nfa.alphabet.append(i)
    return union_nfa

# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    
    dfa1 = nfaToDFA(nfa1)
    dfa1.complement()
    nfa1Complement = dfaToNFA(dfa1)
    
    dfa2 = nfaToDFA(nfa2)
    dfa2.complement()
    nfa2Complement = dfaToNFA(dfa2)
    
    nfa1C_nfa2 = nfaToDFA(union_nfas(nfa1Complement, nfa2))
    nfa1C_nfa2.complement()
    for i in nfa1C_nfa2.is_accepting:
        if nfa1C_nfa2.is_accepting[i] ==True:
            return False
        
    nfa1_nfa2C = nfaToDFA(union_nfas(nfa1, nfa2Complement))
    nfa1_nfa2C.complement()
    for j in nfa1_nfa2C.is_accepting:
        if nfa1_nfa2C.is_accepting[j] == True:
            return False
        
    return True

if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass
    
    # here I edit this function since strRe is not defined here
    def testDFA(strRe, s, expected):
        # convert to nfa first
        re = parse_re(strRe)
        nfa = re.transformToNFA()
        
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s) 
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    #test your NFA:
    # epsilon
    # testNFA('&', '', True)
    # # sym
    # testNFA('a', '', False)
    # testNFA('a', 'a', True)
    # testNFA('a', 'ab', False)
    # # star
    # testNFA('a*', '', True)
    # testNFA('a*', 'a', True)
    # testNFA('a*', 'aaa', True)
    # # or
    # testNFA('a|b', '', False)
    # testNFA('a|b', 'a', True)
    # testNFA('a|b', 'b', True)
    # testNFA('a|b', 'ab', False)
    # testNFA('ab|cd', '', False)
    # testNFA('ab|cd', 'ab', True)
    # testNFA('ab|cd', 'cd', True)
    # # combination
    # testNFA('ab|cd*', '', False)
    # testNFA('ab|cd*', 'c', True)
    # testNFA('ab|cd*', 'cd', True)
    # testNFA('ab|cd*', 'cddddddd', True)
    # testNFA('ab|cd*', 'ab', True)
    # testNFA('((ab)|(cd))*', '', True)
    # testNFA('((ab)|(cd))*', 'ab', True)
    # testNFA('((ab)|(cd))*', 'cd', True)
    # testNFA('((ab)|(cd))*', 'abab', True)
    # testNFA('((ab)|(cd))*', 'abcd', True)
    # testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    
    # testDFA('&', '', True)
    # testDFA('(&)', '', True)
    # testDFA('&', 'a', False)
    # testDFA('a', '', False)
    # testDFA('a', 'a', True)
    # testDFA('a', 'ab', False)
    # testDFA('(a)', 'a', True)
    # testDFA('((a))', 'a', True)
    # testDFA('ab', 'ab', True)
    # testDFA('abc', 'abc', True)
    # testDFA('abcd', 'abcd', True)
    # testDFA('a(bc)d', 'abcd', True)
    # testDFA('a*', '', True)
    # testDFA('a*', 'a', True)
    # testDFA('a*', 'aaa', True)
    # testDFA('a*b*', 'a', True)
    # testDFA('a*b*', 'ab', True)
    # testDFA('a*b*', 'b', True)
    # testDFA('a*b*', 'aba', False)
    # testDFA('a|b', '', False)
    # testDFA('a|b', 'a', True)
    # testDFA('a|b', 'b', True)
    # testDFA('a|b', 'ab', False)
    # testDFA('ab|cd', '', False)
    # testDFA('ab|cd', 'ab', True)
    # testDFA('ab|cd', 'cd', True)
    # testDFA('ab|cd*', '', False)
    # testDFA('ab|cd*', 'c', True)
    # testDFA('ab|cd*', 'cd', True)
    # testDFA('ab|cd*', 'cddddddd', True)
    # testDFA('ab|cd*', 'ab', True)
    # testDFA('((ab)|(cd))*', '', True)
    # testDFA('((ab)|(cd))*', 'ab', True)
    # testDFA('((ab)|(cd))*', 'cd', True)
    # testDFA('((ab)|(cd))*', 'abab', True)
    # testDFA('((ab)|(cd))*', 'abcd', True)
    # testDFA('((ab)|(cd))*', 'cdcdabcd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    # testDFA('((a|b)*|b)*', 'ababb', True)
    
    testEquivalence('((a|b)*|b)*','(b)((a|b)*|b)*',False)
    testEquivalence('a*','aa*',False)
    testEquivalence('a|b', 'a|((a|b)|b)', True)
    testEquivalence('(a|b)*', '(a|((a|b)|b))*', True)
    testEquivalence('&', '&&', True)
    testEquivalence('&', '&&a', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '((ab|cd)*|(de*fg|h(ij)*klm*m*n|q))*', True)
    testEquivalence("a|b", "b|a", True)
    pass
    
