# This module contains algorithms described in the finite automata section in the Handbook of TCS.

empty_word = "epsilon"
halting_state = "halt"

class FiniteAutomata:
    """A finite automata consists of four attributes (Q, I, T, E)"""

    def __init__(self, alphabet: set, states: set, initial_states: set, terminal_states: set, edges: list):
        for edge in edges:
            if edge[1] not in alphabet or edge[0] not in states or edge[2] not in states:
                raise ValueError("Invalid automata")
        if (not initial_states.issubset(states) or not terminal_states.issubset(states)):
            raise ValueError("Invalid automata")
        self.states = states
        self.alphabet = alphabet
        self.initial_states = initial_states
        self.terminal_states = terminal_states
        self.edges = edges  # an edge is a tuple (q, a, p) in QxAxQ

    def next_states(self, state, label):
        return [edge[2] for edge in self.edges if edge[0]==state and edge[1]==label]

    def recognized_word(self, word):
        """A word is recognized if it is the label of a successful path"""
        if (word):
            next_states = [(s, 1) for i in self.initial_states for s in self.next_states(i, word[0])]
            while (next_states):
                (current_state, word_ctr) = next_states.pop()
                if (word_ctr >= len(word)):
                    if (current_state in self.terminal_states):
                        return True
                else:
                    new_frontier = self.next_states(current_state, word[word_ctr])
                    next_states = [(s, word_ctr+1) for s in new_frontier] + next_states
            return False
        else:
            return True  # special empty word, assume always recognizable, check.

    def recognized_set(self):
        """The set of all words recognized by the automata, denoted L(A')"""
        next_states = [(edge[2], edge[1]) for s in self.initial_states for edge in self.edges if edge[0]==s]
        while (next_states):
            (p, word) = next_states.pop()
            if (p in self.terminal_states):
                yield word
            new_frontier = self.next_states(p, word[-1])
            next_states = [(edge[2], word + edge[1]) for s in new_frontier for edge in self.edges if edge[0]==s] + next_states

    def is_determistic(self):
        """An automata is deterministic if there exists at most one edge for each state"""
        if (len(self.initial_states)!=1):
            return False
        sort_dict = {}
        for (p, a, q) in self.edges:
            if (sort_dict.get((p, a)) is None):
                sort_dict[(p, a)] = q
            else:
                return False
        return True
    
    def is_complete(self):
        """An automata is complete if for each (p, a) in QxA, there is at least one q in Q 
        s.t. (p, a, q) in E"""
        for p in self.states:
            for a in self.alphabet:
                if (not self.next_states(p, a)):
                    return False
        return True

class Path:
    """A path is a sequence of consecutive edges"""

    def __init__(self, edges):
        for (idx, edge) in enumerate(edges[0:-1]):
            if (edge[2] != edges[idx+1][0]):
                raise ValueError(f"Path not consecutive {edges}")
        self.edges = edges
            
    def label(self):
        """The label of a path is the word"""
        return "".join([edge[1] for edge in self.edges])

    def is_null_path(self):
        if (len(self.edges) == 1):
            (p, a, q) = self.edges[0]
            return p==q and a==empty_word

    def length(self):
        """The null path has length 0"""
        if (self.is_null_path()):
            return 0
        return len(self.edges)
    
    def origin(self):
        return self.edges[0][0]
    
    def end(self):
        return self.edges[-1][-1]

    def successful(self, finite_automata: FiniteAutomata) -> bool:
        """A path is successful if its origin is an initial state and 
        ends in a terminal state"""
        valid_origin = self.origin() in finite_automata.initial_states
        valid_end = self.end() in finite_automata.terminal_states
        valid_edges = set(self.edges).issubset(set(finite_automata.edges))
        return valid_origin and valid_end and valid_edges
