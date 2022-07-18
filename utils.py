from trie import Trie
from spacy.tokens import Span
import unittest
import string

punct = set(string.punctuation)
def my_sentencizer(lines):
    '''some, but not all, lines are meant to be full sentences 
    but they don't have sentence termination punctuation at the end'''
    out = ''
    for line in lines:
        out += ' '.join(line[:-1])
        word = line[-1]
        if word[-1] in punct or word.lower() == 'and':
            out += ' ' + word + ' '
        else:
            out += ' ' + word + '. '
    
    return out


class LabelHolder:
    def __init__(self, labels=None):
        if not labels:
            labels = []
        self._label_list = [x.upper() for x in labels]
        self._labels = Trie()
        
        self._labels = Trie(self._label_list)

    @property
    def labels(self):
        return self._label_list.copy()

    def remove(self, label):
        lab = label.upper()
        self._label_list.remove(lab)
        self._labels.remove(lab)

    def add(self, label):
        lab = label.upper()
        if lab in self._labels:
            return
        self._labels.add(lab)
        self._label_list.append(lab)

    def __getitem__(self, x):
        if isinstance(x, (int, slice)):
            return self._label_list[x]
        return list(self._labels.super_words(x.upper()))
        
    def __contains__(self, lab):
        return bool(self[lab])
        
    def __str__(self):
        return f'LabelHolder({self._label_list})'
        
    def __bool__(self):
        return bool(self._label_list)
        
    __repr__ = __str__


def label_sent(s, label_holder):
    print([tok for tok in s])
    # assumes the matcher has callback functions that automatically apply labels to a doc when it is used
    lab = None
    len_s = len(s)
    while True:
        slice_ = None
        while True:
            inp = input('''Enter a starting and ending index.
You can also press p to print the sentence, q to quit, l to print valid labels, or sl to print labels on this sentence.
''').lower()
            if inp == 'q':
                return 1
            if inp == 'p':
                print([tok for tok in s])
                continue
            if inp == 'l':
                print(label_holder.labels)
                continue
            if inp == 'sl':
                print([(x.text, x.label_) for x in s.ents])
                continue
            try:
                inp_s = inp.split()
                start, end = None, None
                if inp_s[0][0] == 'n':
                    start = 0
                else:
                    start = int(inp_s[0])
                    if start < 0:
                        start = len_s + start
                        # negative indices don't work for Span(doc, start, end)
                if inp_s[1][0] == 'n':
                    end = len_s
                else:
                    end = int(inp_s[1])
                    if end < 0:
                        end = len_s + end
                slice_ = slice(start, end)
                break
            except Exception as ex:
                print("Invalid input")
        span = s[slice_]
        while True:
            inp = input(f'How do you want to label the span "{span}"? Enter "/" to select a different span instead.\n')
            if inp == '/':
                lab = '/'
                break
            labs = label_holder[inp]
            if labs:
                if isinstance(labs, list):
                    if len(labs) > 1:
                        print(f'There are multiple labels with that prefix: {labs}')
                        continue
                    else:
                        lab = labs[0]
                else:
                    lab = labs
                break
            print('Invalid label')
        if lab == '/':
            continue
        try:
            s.ents = list(s.ents) + [Span(s, start, end, label=lab)]
        except ValueError as ex:
            if "Unable to set" in str(ex):
                print("Can't add a label to that span because it's already labeled.")
    return 0
    

def label_many_sents(sents, labs):
    print("When entering starting and ending indices, you can enter n in place of a number.")
    print("Then it will label through the start or end of the string, depending on which you substitute.")
    if isinstance(labs, LabelHolder):
        lh = labs
    else:
        lh = LabelHolder(labs)
    for s in sents:
        label_sent(s, lh)
        quit = input("q to stop labeling sentences: ")
        if quit == 'q':
            break


class LabelHolderTester(unittest.TestCase):
    def test_add_labels(self):
        lh = LabelHolder()
        lh.add('acorn')
        self.assertIn('ACORN', lh._label_list)
        self.assertIn('ACORN', lh._labels)
        
    def test_init_with_list(self):
        lh = LabelHolder(['acorn'])
        self.assertIn('ACORN', lh._label_list)
        self.assertIn('ACORN', lh._labels)
        
    def init_with_list_then_add(self):
        lh = LabelHolder(['acorn'])
        lh.add('bag')
        self.assertIn('ACORN', lh._label_list)
        self.assertIn('ACORN', lh._labels)
        self.assertIn('BAG', lh._label_list)
        self.assertIn('BAG', lh._labels)
        
    def init_with_list_then_remove(self):
        lh = LabelHolder(['acorn'])
        lh.remove('acorn')
        self.assertEqual(lh._label_list, [])
        self.assertNotIn('acorn', lh._labels)
    
    def test_contains(self):
        lh = LabelHolder(['zoom'])
        self.assertIn('zoom', lh)
        
    def test_does_not_contain(self):
        lh = LabelHolder(['zoom'])
        self.assertNotIn('zom', lh)
    
    def test_labels_property_unrelated(self):
        lh = LabelHolder(['acorn'])
        labs = lh.labels
        labs.append('bag')
        self.assertNotIn('bag', lh)
        self.assertNotIn('BAG', lh)
        
    def test_getitem_int(self):
        lh = LabelHolder(['acorn', 'zoom'])
        self.assertEqual(lh[0], 'ACORN')
        
    def test_getitem_slice(self):
        lh = LabelHolder(['acorn', 'zoom'])
        self.assertEqual(lh[1:], ['ZOOM'])
        
    def test_getitem_string_in_lh(self):
        lh = LabelHolder(['acorn', 'zoom'])
        self.assertEqual(lh['acorn'], ['ACORN'])
        
    def test_getitem_string_not_in_lh_with_super_words(self):
        lh = LabelHolder(['acorn'])
        self.assertEqual(lh['ac'], ['ACORN'])
        
    def test_getitem_string_not_in_lh_no_super_words(self):
        lh = LabelHolder(['acorn'])
        self.assertEqual(lh['b'], [])
        
    def test_getitem_string_not_in_lh_multi_super_words(self):
        lh = LabelHolder(['acorn', 'access'])
        self.assertEqual(lh['a'], ['ACORN', 'ACCESS'])
        
if __name__ == '__main__':
    unittest.main()