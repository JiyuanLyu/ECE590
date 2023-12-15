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
        state_mapping = first.addStatesFrom(second)
        
        for state_id in first.is_accepting:
            if first.is_accepting[state_id]:
                first.addTransition(state_id, state_mapping[second.startS], '&')
                first.is_accepting[state_id] = False

        for state_id, is_accepting in second.is_accepting.items():
            first.is_accepting[state_mapping[state_id]] = is_accepting

        first.alphabet.update(second.alphabet)
        return first
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        child_nfa = self.children[0].transformToNFA()

        star_nfa = NFA()
        start_state = State(0)
        star_nfa.states.append(start_state)
        star_nfa.startS = 0
        star_nfa.is_accepting[start_state.id] = True 

        state_mapping = star_nfa.addStatesFrom(child_nfa)
        star_nfa.addTransition(start_state.id, state_mapping[child_nfa.startS], '&')

        for state_id, is_accepting in child_nfa.is_accepting.items():
            if is_accepting == True:
                star_nfa.addTransition(state_mapping[state_id], state_mapping[child_nfa.startS], '&')
                star_nfa.is_accepting[state_mapping[state_id]] = True

        star_nfa.alphabet = child_nfa.alphabet
        return star_nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        first = self.children[0].transformToNFA()
        second = self.children[1].transformToNFA()

        or_nfa = NFA()

        new_start_state = State(0)
        or_nfa.states.append(new_start_state)
        or_nfa.startS = 0

        state_mapping1 = or_nfa.addStatesFrom(first)
        state_mapping2 = or_nfa.addStatesFrom(second)
        or_nfa.addTransition(new_start_state.id, state_mapping1[first.startS], '&')
        or_nfa.addTransition(new_start_state.id, state_mapping2[second.startS], '&')

        for state_id, is_accepting in first.is_accepting.items():
            if is_accepting:
                or_nfa.is_accepting[state_mapping1[state_id]] = True
        
        for state_id, is_accepting in second.is_accepting.items():
            if is_accepting:
                or_nfa.is_accepting[state_mapping2[state_id]] = True

        or_nfa.alphabet = set(first.alphabet)
        for symbol in second.alphabet:
            or_nfa.alphabet.add(symbol)

        return or_nfa
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
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
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