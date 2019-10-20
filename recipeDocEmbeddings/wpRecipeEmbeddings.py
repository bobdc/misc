#!/usr/bin/env python     

# Read recipe XML files, calculate document vectors for each,
# store the results in a python pickle file.

import glob
import re
import pickle
from flair.embeddings import Sentence, StackedEmbeddings, FlairEmbeddings,WordEmbeddings

import time
import numpy as np
import regex as re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Most of this code is based on
# https://github.com/swapnilg915/cosine_similarity_using_embeddings/blob/master/flair_embeddings.py

# initialize embeddings
glove_embedding = WordEmbeddings('glove')
flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')


class FlairEmbeddings(object):

        def __init__(self):
                self.stop_words = list(stopwords.words('english'))
                self.lemmatizer = WordNetLemmatizer()
                self.stacked_embeddings = StackedEmbeddings(
                        embeddings=[flair_embedding_forward, flair_embedding_backward])

        def word_token(self, tokens, lemma=False):
                tokens = str(tokens)
                tokens = re.sub(r"([\w].)([\~\!\@\#\$\%\^\&\*\(\)\-\+\[\]\{\}\/\"\'\:\;])([\s\w].)", "\\1 \\2 \\3", tokens)
                tokens = re.sub(r"\s+", " ", tokens)
                if lemma:
                        return " ".join([self.lemmatizer.lemmatize(token, 'v') for token in word_tokenize(tokens.lower()) if token not in self.stop_words and token.isalpha()])
                else:
                        return " ".join([token for token in word_tokenize(tokens.lower()) if token not in self.stop_words and token.isalpha()])

        def cos_sim(self, a, b):
                return np.inner(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b)))

        def getFlairEmbedding(self, text):
                sentence = Sentence(text)
                self.stacked_embeddings.embed(sentence)
                return np.mean([np.array(token.embedding) for token in sentence], axis=0)

#################
            
if __name__ == '__main__':
        #recipeDirectory = '/home/bob/temp/wprecipes/data/a-f/'
        #recipeDirectory = '/home/bob/temp/wprecipes/data/g-p/'
        recipeDirectory = '/home/bob/temp/wprecipes/data/q-z/'

        filenameArray = glob.glob(recipeDirectory + 'Cookbook:*')

        print('# start: ' + time.strftime('%H:%M:%S'))

        recipeDataArray = []   # each entry will be an array with the following entries so
        # that they can be referenced like this: recipeDataArray[3][recipeTitleField]
        recipeTitleField = 0
        urlField = 1
        recipeField = 2
        recipeEmbeddingField = 3

        obj = FlairEmbeddings()

        for file in filenameArray:
            recipeContent = ''
            input = open(file, "r")
            for line in input:
                if ("<title>" in line): 
                    title = re.sub(r'^\s*<title>','',line)  # Remove title tags. I'm sure there's some way to 
                    title = re.sub(r'\s*</title>\s*','',title) # do this in one line. 
                recipeContent = recipeContent + line
                if ("<url>" in line): 
                    url = re.sub(r'^\s*<url>','',line)  # Remove url tags. I'm sure there's some way to 
                    url = re.sub(r'\s*</url>\s*','',url) # do this in one line. 
                    ##print(file + ': ' + url)
                recipeContent = recipeContent + line
            input.close()
            recipeDataArray.append([title,url,recipeContent])

        print('# starting to calculate embeddings: ' + time.strftime('%H:%M:%S'))

        # Calculate and save embeddings
        for r in recipeDataArray:
            recipeEmbedding = obj.getFlairEmbedding(r[recipeField])
            r.append(recipeEmbedding)

        pickle.dump(recipeDataArray, open(recipeDirectory + "recipeDataArray.p", "wb" ) )

print('# finished: ' + time.strftime('%H:%M:%S'))
