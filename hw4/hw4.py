import json
from bs4 import BeautifulSoup
import os
import nltk
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
import json
from collections import defaultdict

docs = []
for file_name in filter(lambda x: ".html" in x, os.listdir('hw1\\res')):
    with open("hw1\\res\\"+file_name, 'r', encoding='utf-8') as file:
            docs.append((file_name,file.read()))

texts = []  
for html_content in docs:
    soup = BeautifulSoup(html_content[1], 'html.parser')
    texts.append((html_content[0], soup.get_text()))

possible_tokens = set()
with open("hw2\\res\\tokens.txt", 'r', encoding='utf-8')as file:
    possible_tokens = set(file.read().split('\n'))

idf = defaultdict(int)
lemma_idf= defaultdict(int)
document_tfs = defaultdict(lambda: defaultdict(int))
document_lemma_tfs = defaultdict(lambda: defaultdict(int))
for text in texts:
    tf = defaultdict(int)
    lemma_tf =defaultdict(int)
    tokens = list(filter(lambda x: x in possible_tokens, nltk.word_tokenize(text[1].lower())))
    words_count = len(tokens)
    for token in tokens:
        tf[token] = tokens.count(token)
        
    for token in tf:
        idf[token]+=1
 
    for key in tf:
        lemma = WordNetLemmatizer().lemmatize(key)
        lemma_tf[lemma]+=tf[key]

    for lemma in lemma_tf:
        lemma_idf[lemma]+=1

    document_tfs[text[0]] = tf
    document_lemma_tfs[text[0]] = lemma_tf
res = []
lemma_res=[]
for tfk in document_tfs:
    tf = document_tfs[tfk]
    for k in tf:
        termf =tf[k]/len(tf)
        term_idf =idf[k]/len(texts)
        res.append((k, termf, term_idf, termf*term_idf))

for lemma_tfk in document_lemma_tfs:
    lemma_tf = document_lemma_tfs[lemma_tfk]
    for k in lemma_tf:
        lemma_tf1 = lemma_tf[k]/len(lemma_tf)
        lemma_idf1 =lemma_idf[k]/len(texts)
        lemma_res.append((k, lemma_tf1, lemma_idf1, lemma_tf1*lemma_idf1))

with open("hw4\\res\\tfs.txt", 'w', encoding='utf-8')as file:
    json.dump(res, file)

with open("hw4\\res\\lemma_tfs.txt", 'w', encoding='utf-8')as file:
    json.dump(lemma_res, file)