'''An implementation of the Trie data structure, which enables efficient
searches for strings based on substrings that begin them.
See https://en.wikipedia.org/wiki/Trie.
'''
import unittest
import pprint

class Trie:
    '''An implementation of tries, based on a tree mapping values to dicts.'''
    def __init__(self, words=None):
        self.tree = {}
        if not words:
            return
        self.add_all(words)
    
    def add(self, word, **kwargs):
        assert isinstance(word, str), 'only strings allowed in Trie'
        if 'child' not in kwargs:
            child = self.tree
        else:
            child = kwargs['child']
        if not word:
            child[''] = {}
            return
        child.setdefault(word[0], {})
        self.add(word[1:], child = child[word[0]])
        
    def add_all(self, words):
        for word in words:
            self.add(word)
    
    def remove(self, word: str) -> bool:
        """Eagerly remove the word from the trie rooted at `root`.
    Return whether the trie rooted at `root` is now empty.
    THIS METHOD IS SLIGHTLY MODIFIED FROM THE delete() METHOD IN THE WIKIPEDIA
    ARTICLE https://en.wikipedia.org/wiki/Trie.
        """
        def _delete(child: dict, word: str, d: int) -> bool:
            """Clear the node corresponding to word[d], and delete the child word[d+1]
            if that subtrie is completely empty, and return whether `node` has been
            cleared.
            """
            if d == len(word):
                try:
                    del child['']
                except:
                    raise KeyError(f"{repr(word)} is not in this Trie")
            else:
                c = word[d]
                try:
                    if _delete(child[c], word, d+1):
                        del child[c]
                except:
                    raise KeyError(f"{repr(word)} is not in this Trie.")
            # Return whether the subtrie rooted at `node` is now completely empty
            return len(child) == 0
        return _delete(self.tree, word, 0)
    
    def __contains__(self, word, **kwargs):
        if 'child' not in kwargs:
            child = self.tree
        else:
            child = kwargs['child']
        if not word:
            if '' in child:
                return True
            return False
        if word[0] in child:
            return self.__contains__(word[1:], child = child[word[0]])
    
    def super_words(self, word, **kwargs):
        if 'curword' not in kwargs:
            curword = ''
        else:
            curword = kwargs['curword']
        if 'child' not in kwargs:
            child = self.tree
        else:
            child = kwargs['child']
        if word == '':
            for val in child:
                if val == '':
                    yield curword
                yield from self.super_words('', 
                                            curword = curword + val,
                                            child = child[val])
            return
        if word[0] in child:
            yield from self.super_words(word[1:], 
                                        curword = curword + word[0],
                                        child = child[word[0]])
        return
    
    def __str__(self):
        return f"Trie({pprint.pformat(self.tree, width = 40)})"
        

class TrieTester(unittest.TestCase):
    def test_add_contains(self):
        t = Trie()
        t.add('ab')
        self.assertIn('ab', t)
        
    def test_remove(self):
        t = Trie()
        t.add('ab')
        t.remove('ab')
        self.assertNotIn('ab', t)
    
    def test_remove_not_in_t(self):
        t = Trie()
        with self.assertRaisesRegex(KeyError, "not in this Trie"):
            t.remove('ab')
            
    def test_substring_not_in_t(self):
        t = Trie()
        t.add('aba')
        with self.assertRaisesRegex(KeyError, "not in this Trie"):
            t.remove('ab')
            
    def test_remove_substring(self):
        t = Trie()
        t.add('aba')
        t.add('ab')
        t.remove('ab')
        self.assertIn('aba', t)
        
    def test_remove_superstring(self):
        t = Trie()
        t.add('aba')
        t.add('ab')
        t.remove('aba')
        self.assertIn('ab', t)
        
    def test_remove_unrelated_string(self):
        t = Trie()
        t.add('a')
        t.add('b')
        t.remove('b')
        self.assertIn('a', t)
        
    def test_empty_string(self):
        t = Trie()
        t.add('')
        self.assertIn('', t)
        
    def test_remove_empty_string(self):
        t = Trie()
        t.add('')
        t.add('ab')
        t.remove('')
        self.assertNotIn('', t)
        self.assertIn('ab', t)
        
    def test_super_words_none(self):
        t = Trie()
        t.add('a')
        self.assertEqual(list(t.super_words('b')), [])
        
    def test_super_words_word_in_t_one_result(self):
        t = Trie()
        t.add('ab')
        self.assertEqual(list(t.super_words('ab')), ['ab'])
    
    def test_super_words_word_not_in_t_one_result(self):
        t = Trie()
        t.add('ab')
        self.assertEqual(list(t.super_words('a')), ['ab'])
        
    def test_super_words_word_in_t_multi_results(self):
        t = Trie()
        t.add('dog')
        t.add('dogged')
        t.add('abacus')
        self.assertEqual(set(t.super_words('dog')), {'dog', 'dogged'})
        
    def test_super_words_word_not_in_t_multi_results(self):
        t = Trie()
        t.add('dog')
        t.add('abeyance')
        t.add('abacus')
        self.assertEqual(set(t.super_words('ab')), {'abacus', 'abeyance'})
        
    def test_init_with_list(self):
        t = Trie(['a', 'ab'])
        self.assertEqual(set(t.super_words('')), {'a', 'ab'})
        

if __name__ == '__main__':
    unittest.main()