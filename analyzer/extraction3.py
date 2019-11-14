# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1S3jB1Lkz2b4vwkwQ9dz0SA4ep2BsssiR

"""
# %%
import glob
import json
import os
import re
import sys
from collections import Counter

import en_core_web_sm
import networkx as nx
import nltk
import numpy as np
import pandas as pd
import spacy
# Gensim contains word2vec models and processing tools
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from spacy import displacy

from nextword import get_wordgroup, get_wordgroup_by
from scrapper import process_urls, trigger_remote
from utilities import remove_stopwords, sanitize

# %%
project_path = os.getcwd() + os.path.sep
# %cd  "/content/drive/My Drive/DLCP/Fake News Challenge/"
print("project directory set to " + project_path)

# %%
# one time execution
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')  # download the corous
nltk.download('averaged_perceptron_tagger')  # Download the tagger
print("downloaded nltk modules")

# %%
stop_words = stopwords.words('english')
spacy_nlp = spacy.load('en_core_web_sm')
nlp = en_core_web_sm.load()

print("configured stopwords and spacy")

# %%
word_embeddings = {}
with open(project_path + 'glove.6B.300d.txt', encoding='utf-8') as dFile:
    for line in dFile:
        values = line.split()
        word_embeddings[values[0]] = np.asarray(
            values[1:], dtype='float32')

# This is a GloVe model
glove_file = datapath(project_path + 'glove.6B.300d.txt')
tmp_file = get_tmpfile(project_path + 'word2vec.glove.6B.300d.txt')

# Converting the GloVe file into a Word2Vec file
if not os.path.exists(tmp_file):
    glove2word2vec(glove_file, tmp_file)

model = KeyedVectors.load_word2vec_format(tmp_file)
print("glove setup complete")


# %%
def process(art):
    print("processing " + str(art))
    sentences = []
    for s in getattr(art, 'fullarticle'):
        sentences.append(sent_tokenize(sanitize(s)))

    sentences = [y for x in sentences for y in x]  # flatten list

    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]

    clean_sentences = [remove_stopwords(
        r.split(), stop_words) for r in clean_sentences]

    print("generating vectors")
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((300,)))
                     for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((300,))
        sentence_vectors.append(v)

    sim_mat = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(
                    1, 300), sentence_vectors[j].reshape(1, 300))[0, 0]

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    article_length = len(ranked_sentences)
    print("Article length: " + str(article_length))

    if article_length < 6:
        summary_length = article_length
    else:
        summary_length = article_length//3

    # print(summary_length)

    summary = ''
    for i in range(summary_length):
        summary = print(ranked_sentences[i][1])
    # print(summary)

    animal_found = []
    animal_volume = []
    animal_found_loc = []
    animal_found_city = []
    animal_money = []

    list_of_probable_word = ['seize', 'kill', 'carcass', 'poaching']
    all_word_list = []
    for i in list_of_probable_word:
        all_word_list += model.most_similar(positive=[i])

    animal_list = ['Tiger', 'Elephant', 'Rhino', 'rhino horn']

    summarized_sent = ''
    for i in ranked_sentences:
        summarized_sent += str(i[1])
    print(summarized_sent)

    for word in all_word_list:
        for individual_sent in ranked_sentences:
            if word[0].lower() in individual_sent[1].lower():
                # print(individual_sent[1])
                doc = nlp(individual_sent[1])
                name_entity_lisgt = [(X.text, X.label_) for X in doc.ents]
                # print(name_entity_lisgt)

                # Find animal Name

                for animal in animal_list:
                    if animal.lower() in individual_sent[1].lower():
                        animal_found.append(animal)

                for entity in name_entity_lisgt:
                    if 'CARDINAL' == entity[1]:
                        # print (entity[0])
                        get_wordgroup(individual_sent[1], entity[0], -1)
                        # type(indices)
                        # print(individual_sent[1].split()[(indices[0]-1):(indices[0]+2)])
                        animal_volume.append(get_wordgroup(
                            individual_sent[1], entity[0], -1))

                    if 'FAC' == entity[1]:
                        animal_found_loc.append(entity[0])

                    if 'GPE' == entity[1]:
                        animal_found_city.append(entity[0])

                    if 'QUANTITY' == entity[1]:
                        animal_volume.append(entity[0])

                    if 'MONEY' == entity[1]:
                        animal_money.append(entity[0])

    # print ( "-----------------")
    print(animal_found)
    print(animal_volume)
    print(animal_found_loc)
    print(animal_found_city)
    print(animal_money)

    # article["summary"] = summary
    # article["animal_found"] = animal_found
    # article["animal_volume"] = animal_volume
    # article["animal_found_loc"] = animal_found_loc
    # article["animal_found_city"] = animal_found_city
    # article["animal_money"] = animal_money

    return


# %%
df = trigger_remote("rhinos and poaching")
print(df)

# loop dataframe
for searchData in df.itertuples(index=False):
    print(searchData)
