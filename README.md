# Heavy metal text analytics with spaCy
This is a project I did in May 2022 for a course in the University of Wisconsin Data Science Masters program.

My goal in this project was to do some fun investigation of themes in the lyrics of the heavy metal band Iron Maiden. I used BeautifulSoup to scrape lyrics off of [darklyrics.com](darklyrics.com) (see **scrape_darklyrics.py** for script) and then did some analysis of the text to learn about the relative importances of the themes of *death*, *light*, and *time* in Iron Maiden studio albums over the course of their long discography.

See **iron maiden text analysis.docx** for my writeup, **analyze_iron_maiden.ipynb** and **visualize_iron_maiden.ipynb** for my data analysis and construction of visualizations, **utils.py** for some utilities allowing easy terminal-based labeling of spans in documents, and **trie.py** for my implemenation of the Trie data structure (used in the LabelHolder class of utils.py, partially based on code snippets on the Wikipedia article).

I also have four Jupyter notebooks (labeled *spacy dot io CHAPTER x*) created by following along with the spaCy introduction course on [spacy.io](spacy.io).