from collections import defaultdict 
import math
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as sw
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stopwords = set(sw.words('english'))

def getIndex(path):
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

index = getIndex("hw3\\res\\index.json")



def get_doc_vector(doc_id, index):
    doc_vector = defaultdict(int)
    for term in index.keys():
        tf = index[term].get(doc_id, 0)
        if tf > 0:
            idf = math.log10(len(index) / len(index[term]))
            doc_vector[term] = tf * idf
    return doc_vector

def get_query_vector(query, index):
    query_vector = defaultdict(int)
    query_terms = preprocess(query)
    for term in query_terms:
        if term in index:
            idf = math.log10(len(index) / len(index[term]))
            query_vector[term] += idf
    return query_vector

def cosine_similarity(a, b):
    dot_product = sum(a.get(term, 0) * b.get(term, 0) for term in set(a) & set(b))
    norm_a = math.sqrt(sum(a.get(term, 0) ** 2 for term in a))
    norm_b = math.sqrt(sum(b.get(term, 0) ** 2 for term in b))
    norm = norm_a * norm_b
    if norm == 0:
        return 0
    return dot_product / (norm_a * norm_b)

def search(query, index, documents):
    query_vector = get_query_vector(query, index)
    results = []
    for doc_id in documents:
        doc_vector = get_doc_vector(doc_id, index)
        similarity = cosine_similarity(query_vector, doc_vector)
        if similarity > 0:
            results.append((doc_id, similarity))
    return sorted(results, key=lambda x: x[1], reverse=True)

def getSearch(query):
    return search(query, index, documents)
documents = set()
for k in index:
    for doc in index[k].keys():
        documents.add(doc)
#query = "concussions"
#print(search(query, index, documents))
