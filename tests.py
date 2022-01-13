import unittest
from finite_automata import *

class TestPathMethods(unittest.TestCase):
    alphabet = {'a', 'b'}
    states = {1, 2, 3}
    automata = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
        
    def test_constructor(self):
        with self.assertRaises(ValueError):
            Path([(1, 'a', 1), (2, 'b', 3)])
        Path([(1, 'a', 2), (2, 'b', 3)])
        Path([(1, 'a', 2)])
        Path([(1, 'a', 1)])
        Path([(1, 'a', 1), (1, 'a', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])

    def test_label(self):
        p1 = Path([(1, 'a', 1), (1, 'a', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
        self.assertEqual(p1.label(), 'aaaab')

    def test_successful(self):
        self.assertFalse(Path([(1, 'a', 1), (1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3)]).successful(self.automata))
        self.assertFalse(Path([(1, 'a', 1), (1, 'b', 1), (1, 'c', 1), (1, 'a', 2), (2, 'b', 3)]).successful(self.automata))
        self.assertTrue(Path([(1, 'a', 1), (1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)]).successful(self.automata))
        self.assertFalse(Path([(1, 'a', 1), (1, 'b', 1), (1, 'a', 1), (1, 'a', 2)]).successful(self.automata))

    def test_null_path(self):
        self.assertFalse(Path([(1, 'a', 1), (1, 'b', 1), (1, 'a', 1), (1, 'a', 2)]).is_null_path())
        self.assertFalse(Path([(1, 'a', 1)]).is_null_path())
        self.assertTrue(Path([(1, 'epsilon', 1)]).is_null_path())
    
    def test_length(self):
        self.assertEqual(Path([(1, 'epsilon', 1)]).length(), 0)
        self.assertEqual(Path([(1, 'a', 1)]).length(), 1)
        self.assertEqual(Path([(1, 'a', 1), (1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3)]).length(), 6)
        
class TestFiniteAutomata(unittest.TestCase):
    # alphabet = {'a', 'b'}
    # states = {1, 2, 3}
    # automata = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
    
    def test_recognized_words_one_state(self):
        """Recognize a string that contains only a"""
        alphabet = {'a'}
        states = {1}
        automata = FiniteAutomata(alphabet, states, {1}, {1}, [(1, 'a', 1)])
        self.assertTrue(automata.recognized_word('aaaaaaaaa'))
        self.assertTrue(automata.recognized_word('a'))
        self.assertFalse(automata.recognized_word('aaaaaaaaab'))

    def test_recognized_words_multiple_states(self):
        """Recognize a string that ends with a,b"""
        alphabet = {'a', 'b'}
        states = {1, 2, 3}
        automata = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1)])
        self.assertTrue(automata.recognized_word('aaaaaaaaab'))
        self.assertTrue(automata.recognized_word('ab'))
        self.assertTrue(automata.recognized_word('bbbbbbbbbbaaaaaabbbbbbbaaaab'))
        self.assertFalse(automata.recognized_word('aaaaaaaaaa'))
        self.assertFalse(automata.recognized_word('a'))
        self.assertFalse(automata.recognized_word('b'))
        self.assertFalse(automata.recognized_word('cbabdnejue'))
        self.assertFalse(automata.recognized_word('aaaaabbcbbbbaaaaab'))

    def test_deterministic(self):
        alphabet = {'a', 'b'}
        states = {1, 2, 3}
        automata1 = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1)])
        self.assertTrue(automata1.is_determistic())
        automata2 = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
        self.assertFalse(automata2.is_determistic())
        automata3 = FiniteAutomata(alphabet, states, {1, 2}, {3}, [(1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
        self.assertFalse(automata3.is_determistic())

    def test_complete(self):
        alphabet = {'a', 'b'}
        states = {1, 2, 3}
        automata1 = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1)])
        self.assertTrue(automata1.is_complete())
        automata2 = FiniteAutomata(alphabet, states, {1}, {3}, [(1, 'b', 1), (1, 'a', 1), (1, 'a', 2), (2, 'b', 3)])
        self.assertFalse(automata2.is_complete())

    def test_recognized_set(self):
        alphabet = {'a'}
        states = {1}
        automata = FiniteAutomata(alphabet, states, {1}, {1}, [(1, 'a', 1)])
        recognized_set = automata.recognized_set()
        for i in range(20):
            self.assertTrue(next(recognized_set))

        alphabet2 = {'a', 'b'}
        states2 = {1, 2, 3}
        automata2 = FiniteAutomata(alphabet2, states2, {1}, {3}, [(1, 'b', 1), (1, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1)])
        recognized_set2 = automata2.recognized_set()
        for i in range(20):
            # print(next(recognized_set2))
            self.assertTrue(next(recognized_set2))


if __name__ == '__main__':
    unittest.main()