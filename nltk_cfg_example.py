from nltk import Nonterminal, nonterminals, Production, CFG
import nltk
from nltk.treeprettyprinter import TreePrettyPrinter

math_cfg = CFG.fromstring('''
expr -> signed_num | lparen expr rparen | expr binop expr
signed_num -> uminus num | num
num -> int | int dot int | int exp_part | int dot int exp_part
int -> digit | digit int
digit -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
binop -> '*' | '+' | '-' | '^' | '==' | '>' | '<' | '/'
exp_part -> e int | e uminus int
e -> 'e' | 'E'
lparen -> '('
rparen -> ')'
dot -> '.'
uminus -> '-'
''')

print(f"{math_cfg.productions(rhs = 'int') = }")

parser = nltk.ChartParser(math_cfg)

nums_parens = ['4', '/', '(', '5', '+', '-', '2', '.', '1', ')', '==', '4', '9']

nums = ['4', '/', '5', '+', '-', '2', '.', '1', '==', '4', '9']

nums_trees = list(parser.parse(nums))

nums2_trees = list(parser.parse(nums_parens))

prntr = TreePrettyPrinter(nums_trees[0])
print(f'The parser can parse {nums}\n{prntr.text()}')
prntr2 = TreePrettyPrinter(nums_trees[1])
print(f'An alternate parse of {nums}:\n{prntr2.text()}')
prntr_nums2 = TreePrettyPrinter(nums2_trees[0])
print(f'The parser parses {nums_parens}\n{prntr_nums2.text()}')