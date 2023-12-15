from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        pass
    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return states
    
    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        # I implement this method based on the given method problematic()
        # In the problematic(), the current state is pop from the last element of queue
        # it follows the Last In First Out and it's a stack not a queue
        # So problematic() used DFS to figure out if the string is in the Language
        # Here I would like to use BFS instead and always pop the first element of queue
        
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            # Here I would like to use First In First Out to visit the states
            # which is based on BFS
            currS, pos = queue.pop(0)
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass
        
        
    # The problematic function that need to be fixed
    def problematic(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop()
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass
