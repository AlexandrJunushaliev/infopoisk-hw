import json
from bs4 import BeautifulSoup
import os
import nltk
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
import json

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
    dump = dict(zip(inverted_index.keys(), map(list, inverted_index.values())))
    with open(path, "w") as f:
        json.dump(dump, f)

def loadIndex(path):
    with open(path, "r") as f:
        return json.load(f)

def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [w.lower() for w in tokens if w.isalpha() and w.lower() not in stopwords and len(w) > 2 and not any(char.isdigit() for char in w)]
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    filtered_lemmas = [lemma for lemma in lemmas if lemma not in stopwords]
    return filtered_lemmas

def preprocessSoft(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmas

def createIndex(documents):
    index = {}
    for i, doc in enumerate(documents):
        lemmas = preprocess(doc[1])
        for lemma in lemmas:
            if lemma not in index:
                index[lemma] = set()
            index[lemma].add(doc[0])
    return index

def search(query, index):
    query_tokens = preprocessSoft(query)
    print (query_tokens)
    result_docs = set()
    i = 0
    while i < len(query_tokens):
        token = query_tokens[i]
        
        if token == 'or':
            or_token = query_tokens[i+1]
            if or_token in index:
                or_docs = set(index[or_token])
                result_docs |= or_docs
            i+=1
        elif token == 'and':
            and_token = query_tokens[i+1]
            if and_token in index:
                and_docs = set(index[and_token])
                result_docs &= and_docs
            i+=1
        elif token in index:
            result_docs = set(index[token])
        i+=1
    
    return result_docs

index = getIndex("hw3\\res\\index.json")
print(search("bennet AND concussion", index ))
