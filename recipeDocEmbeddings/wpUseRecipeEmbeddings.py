#!/usr/bin/env python     

# Read the pickle files full of recipe document embeddings stored by
# wpRecipeEmbeddings.py into one big array, # calculate all cosine
# similarity parings, output RDF about the result.

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
        recipeDirectory = '/home/bob/temp/wprecipes/data/test/'

        filenameArray = glob.glob(recipeDirectory + 'Cookbook:*')

        # each entry will be an array with the following entries so
        # that (e.g.) the title of recipe number 3 can be referenced
        # like this: recipeDataArray[3][recipeTitleField]
        
        recipeTitleField = 0
        urlField = 1
        recipeField = 2
        recipeEmbeddingField = 3

        print('# start: ' + time.strftime('%H:%M:%S'))

        obj = FlairEmbeddings()

        recipeDirectory = '/home/bob/temp/wprecipes/data/a-f/'
        a_f_array = pickle.load( open( recipeDirectory + "recipeDataArray.p", "rb" ))

        recipeDirectory = '/home/bob/temp/wprecipes/data/g-p/'
        g_p_array = pickle.load( open( recipeDirectory + "recipeDataArray.p", "rb" ))

        recipeDirectory = '/home/bob/temp/wprecipes/data/q-z/'
        q_z_array = pickle.load( open( recipeDirectory + "recipeDataArray.p", "rb" ))

        recipeDataArray = a_f_array + g_p_array + q_z_array

        print('# starting comparisons: ' + time.strftime('%H:%M:%S'))

        # output header of RDF
        print("@prefix d: <http://learningsparql.com/data#> .")
        print("@prefix m: <http://learningsparql.com/model#> .")
        print("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")

        # Find the cosine similarity of all the combinations
        recipesToCompare = len(recipeDataArray)  # or some small number for tests
        i1 = 0
        while i1 < recipesToCompare:
            title = recipeDataArray[i1][recipeTitleField].replace('\"','\\"')
            print('<' + recipeDataArray[i1][urlField] + '>  dc:title "' + title + '" .')
            i2 = i1 + 1;
            while i2 < recipesToCompare:
                # output triples like [ m:doc d:0, d:1 ; m:recipeCosineSim 0.8249611 ] 
                recipeCosineSim = \
                obj.cos_sim(recipeDataArray[i1][recipeEmbeddingField],
                            recipeDataArray[i2][recipeEmbeddingField])

                print('[ m:doc <' + recipeDataArray[i1][urlField] +
                      '>, <' + recipeDataArray[i2][urlField] +
                      '> ; m:recipeCosineSim ' + str(recipeCosineSim) + ' ] . ')
                i2 += 1
            i1 += 1

print('# finished: ' + time.strftime('%H:%M:%S'))

