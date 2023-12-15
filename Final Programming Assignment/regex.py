from re import T
from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children: 
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        first = self.children[0].transformToNFA()
        second = self.children[1].transformToNFA()
        len1 = len(first.states)
        first.addStatesFrom(second)
        for i in range(len1):
            if first.is_accepting[i]:
                first.addTransition(first.states[i],first.states[len1])
        for i in range(len1):
            first.is_accepting[i] = False
        for i in second.alphabet:
            if i not in first.alphabet:
                first.alphabet.append(i)    
        return first
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        star_nfa = self.children[0].transformToNFA()
        star_length = len(star_nfa.states)
        for i in range(1, star_length):
            if star_nfa.is_accepting[i]:
                star_nfa.addTransition(star_nfa.states[i], star_nfa.states[0])
        star_nfa.is_accepting[0]=True
        return star_nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        # first = self.children[0].transformToNFA()
        # second = self.children[1].transformToNFA()
        # new_start_state = State(0)
        # first.startS = new_start_state.id
        # first.states.insert(0, new_start_state)
        # second.startS = new_start_state.id
        # second.states.insert(0, new_start_state)
        # offset = len(first.states)
        # for state in second.states:
        #     state.id += offset
        # first.states.extend(second.states)

        # # Merge the alphabets
        # first.alphabet = set(first.alphabet).union(second.alphabet)
        # first.addTransition(new_start_state, first.states[1])
        # first.addTransition(new_start_state, first.states[offset + 1])
        # for state_id in range(offset, offset + len(second.states)):
        #     if state_id - offset in second.is_accepting and second.is_accepting[state_id - offset]:
        #         first.is_accepting[state_id] = True
        
        first = self.children[0].transformToNFA()
        second = self.children[1].transformToNFA()
        first_length = len(first.states)
        
        first.addStatesFrom(second)
        first.addTransition(first.states[0], first.states[first_length])
        for i in second.alphabet:
            if i not in first.alphabet:
                first.alphabet.append(i)
        return first
    pass

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    # 1c implementation
    def transformToNFA(self):
        nfa = NFA()
        start_state = State(0)
        accept_state = State(1)
        nfa.states.extend([start_state, accept_state])
        start_state.transition[self.sym] = [accept_state]

        nfa.is_accepting[0] = False
        nfa.is_accepting[1] = True
        if self.sym not in nfa.alphabet:
            nfa.alphabet.append(self.sym)
        return nfa
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    # 1b implementation
    def transformToNFA(self):
        nfa = NFA()
        epsilon = State(0)
        nfa.states.append(epsilon)
        nfa.is_accepting[0] = True
        return nfa
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*': # type: ignore
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon") # type: ignore
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'): # type: ignore
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()