import numpy as np
import pandas as pd
import pickle
import string
import tensorflow as tf
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import tensorflow_hub as hub
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
#data preparation
def preprocess_sentences(input_sentences):
    output=[]
    lemmatizer = WordNetLemmatizer()
    stop_words = ['be', 'is', 'are', 'and', 'the', 'an', 'a', 'was', 'were', 'they', 'you', 'we', 'you', 'he',
                  'she', 'i', 'me', 'her', 'his', 'to', 'from', 'can', 'would', 'will', 'does', 'do', 'of', 'for', 'with', ]

    for sentence in input_sentences:
        sentence = re.sub(r"ToMV", "tomato mosaic virus", sentence)
        sentence = re.sub(r"TMV", "tobacco mosaic virus", sentence)
        sentence = re.sub(r"CMV", "cucumber mosaic virus", sentence)
        for p in string.punctuation:
            sentence = sentence.replace(p, '')

        sentence= sentence.lower()

        sentence= ' '.join([w for w in sentence.split() if w not in stop_words])

        sentence = ' '.join([lemmatizer.lemmatize(w) for w in sentence.split()])

        output.append(sentence)
    return output
# dataset = pd.read_csv("Q&A for mosaic.csv", encoding='utf-8')
# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model = hub.load(module_url)
# def embed(input):
#   return model(preprocess_sentences([input]))
# dataset['Question_Vector'] = dataset.Questions.map(embed)
# dataset['Question_Vector'] = dataset.Question_Vector.map(np.array)
# pickle.dump(dataset, open('dataset.pkl', 'wb'))

class DialogueManager(object):
    def __init__(self):
        #self.model = tf.saved_model.load("../data/tmp/mobilenet/1/")
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.dataset = pickle.load(open('dataset.pkl', mode='rb'))
        self.questions = self.dataset.Questions
        self.QUESTION_VECTORS = np.array(self.dataset.Question_Vector)
        self.COSINE_THRESHOLD = 0.5
        self.chitchat_bot = ChatBot("Chatterbot")
        trainer = ChatterBotCorpusTrainer(self.chitchat_bot)
        trainer.train("chatterbot.corpus.english")

    def embed(self,input):
        return self.model(preprocess_sentences([input]))


    def cosine_similarity(self,v1, v2):
        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)
        if (not mag1) or (not mag2):
            return 0
        return np.dot(v1, v2) / (mag1 * mag2)


    def semantic_search(self, query, data, vectors):
        query_vec = np.array(self.embed(query))
        res = []
        for i, d in enumerate(data):
            qvec = vectors[i].ravel()
            sim = self.cosine_similarity(query_vec, qvec)
            res.append((sim, d[:100], i))
        return sorted(res, key=lambda x: x[0], reverse=True)

    def generate_answer(self, question):
        #Choose the most similar question in database
        most_relevant_row = self.semantic_search(question, self.questions, self.QUESTION_VECTORS)[0]
        print(most_relevant_row)
        if most_relevant_row[0][0]>=self.COSINE_THRESHOLD:
            answer = self.dataset.Questions[most_relevant_row[2]]+' \n '+self.dataset.Answer[most_relevant_row[2]]
        else:
            answer = self.chitchat_bot.get_response(question)
        return answer



