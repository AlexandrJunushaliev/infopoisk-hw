import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

docs = []
for file_name in filter(lambda x: ".html" in x, os.listdir('hw1\\res')):
    with open("hw1\\res\\"+file_name, 'r', encoding='utf-8') as file:
            docs.append(file.read())    

stop_words = set(nltk.corpus.stopwords.words('english'))
tokens = []
for doc in docs:
    words = word_tokenize(doc)
    filtered_words = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words and len(w) > 2 and not any(char.isdigit() for char in w)]
    tokens.extend(filtered_words)
tokens = list(set(tokens))

lemmatizer = WordNetLemmatizer()
lemmas = defaultdict(list)
for token in tokens:
    lemma = lemmatizer.lemmatize(token)
    lemmas[lemma].append(token)

with open('hw2\\res\\tokens.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(tokens))

with open('hw2\\res\\lemmas.txt', 'w', encoding='utf-8') as file:
    for lemma, token_list in lemmas.items():
        file.write(f'{lemma}: {", ".join(token_list)}\n')