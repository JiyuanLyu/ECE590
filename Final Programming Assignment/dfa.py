import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        s1.transition[sym] = [s2]
        pass 
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for key in self.is_accepting:
            self.is_accepting[key] = not self.is_accepting[key]
        pass
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        curr = 0
        for c in string:
            if c not in self.states[curr].transition:
                return False;
            else:
                curr = self.states[curr].transition[c][0].id
        return self.is_accepting[curr]
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        queue = [0]
        str = [""]
        visited = []
        while queue != []:
            curr_sta = queue.pop(0)
            curr_str = str.pop(0)
            if self.is_accepting[curr_sta]:
                return curr_str
            if curr_sta not in visited:
                visited.append(curr_sta)
            for element in self.states[curr_sta].transition:
                queue.append(self.states[curr_sta].transition[element][0].id)
                str.append(curr_str + element)
        return "Fail to find the shortest string!"
    pass