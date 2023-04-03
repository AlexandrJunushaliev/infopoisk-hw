import json
from bs4 import BeautifulSoup
import os
import nltk
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
import json
from collections import defaultdict

nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
stopwords = set(sw.words('english'))

def getIndex(path):
    if os.path.isfile(path):
        return loadIndex(path)
    else:
        docs = []
        for file_name in filter(lambda x: ".html" in x, os.listdir('hw1\\res')):
            with open("hw1\\res\\"+file_name, 'r', encoding='utf-8') as file:
                    docs.append((file_name,file.read()))

        texts = []  
        for html_content in docs:
            soup = BeautifulSoup(html_content[1], 'html.parser')
            texts.append((html_content[0], soup.get_text()))
        index = createIndex(texts)
        saveIndex(path, index)
        return index

def saveIndex(path, inverted_index):
    with open(path, "w") as f:
        json.dump(inverted_index, f)

def loadIndex(path):
    with open(path, "r") as f:
        return json.load(f)

def preprocess(text, need_lemma=True):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [w.lower() for w in tokens if w.isalpha() and w.lower() not in stopwords and len(w) > 2 and not any(char.isdigit() for char in w)]
    if (need_lemma):
        lemmas = [lemmatizer.lemmatize(token) for token in tokens]
        filtered_lemmas = [lemma for lemma in lemmas if lemma not in stopwords]
        return filtered_lemmas
    return tokens

def preprocessSoft(text, need_lemma=True):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    if need_lemma:
        lemmas = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmas
    return tokens

def createIndex(documents):
    index = {}
    for i, doc in enumerate(documents):
        words = preprocess(doc[1], True)
        for word in words:
            if word not in index:
                index[word] = defaultdict(int)
            index[word][doc[0]] += 1
    return index

def search(query, index):
    query_tokens = preprocessSoft(query, True)
    print (query_tokens)
    result_docs = set()
    i = 0
    while i < len(query_tokens):
        token = query_tokens[i]
        if token == 'not':
            res = []
            unwanded_docs = set(index[query_tokens[i+1]].keys())
            for k in index.keys():
                res.append(index[k].keys())
            result_docs = set()
            for x in res:
                for j in x:
                    if j not in unwanded_docs:
                        result_docs.add(j)
            i+=1
        elif token == 'or':
            or_token = query_tokens[i+1]
            if or_token == "not":
                res = []
                unwanded_docs = set(index[query_tokens[i+2]].keys())
                for k in index.keys():
                        res.append(index[k].keys())
                for x in res:
                    for j in x:
                        if j not in unwanded_docs:
                            result_docs.add(j)
                i+=1
            elif or_token in index:
                or_docs = set(index[or_token].keys())
                result_docs |= or_docs
            i+=1
        elif token == 'and':
            and_token = query_tokens[i+1]
            if and_token == "not":
                res = []
                unwanded_docs = set(index[query_tokens[i+2]].keys())
                for k in index.keys():
                    res.append(index[k].keys())
                res_set = set()
                for x in res:
                    for j in x:
                        if j not in unwanded_docs:
                            res_set.add(j)
                result_docs &= res_set
                i+=1
            if and_token in index:
                and_docs = set(index[and_token].keys())
                result_docs &= and_docs
            i+=1
        elif token in index:
            result_docs = set(index[token].keys())
        i+=1
    
    return result_docs

index = getIndex("hw3\\res\\index.json")
print(search("concussions", index ))
