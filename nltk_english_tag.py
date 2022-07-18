import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

txt = "My name is Mark, and I'm here with my 3-year-old dog Bochy. He is a good boy."
sents = sent_tokenize(txt)
sentoks = [word_tokenize(sent) for sent in sents]
tagged = [nltk.pos_tag(sent) for sent in sentoks]

print(f'{tagged = }')