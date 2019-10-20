#!/home/bob/anaconda3/bin/python

import pickle
import numpy as np
import datetime

from flair.embeddings import Sentence, StackedEmbeddings, FlairEmbeddings,WordEmbeddings, DocumentPoolEmbeddings
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# following for easier referencing of entries in array, e.g. recipeDataArray[3][title]
recipeTitleField = 0
recipeXMLField = 1
recipePlainTextField = 2
recipeXMLEmbeddingField = 3
recipePlainTextEmbeddingField = 4
recipeTitleEmbeddingField = 5

# initialize embeddings
glove_embedding = WordEmbeddings('glove')
flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')

## probably won't need this
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

# I tried moving the class to a separate file instead of defining it the same way here and in readfiles.py but had trouble
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

    obj = FlairEmbeddings()

    recipeDataArray = pickle.load( open( "recipeDataArray.p", "rb" ) )

    # Output triples about the titles
    print("@prefix d: <http://learningsparql.com/data#> .")
    print("@prefix m: <http://learningsparql.com/model#> .")
    print("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")

    # Find the cosine similarity of all the combinations
    recipesToCompare = len(recipeDataArray)  # or some small number for tests

    i1 = 0
    while i1 < recipesToCompare:
        
        title = recipeDataArray[i1][recipeTitleField].replace('\"','\\"')
        print('d:' + str(i1) + ' dc:title "' + title + '" .')
        i2 = i1 + 1;
        while i2 < recipesToCompare:
            # output triples like [ m:doc d:0, d:1 ; m:cosinsim 0.8249611 m:type "xml" ]  PLUS MORE SHOWN BELOW
            XMLCosinSim = \
            obj.cos_sim(recipeDataArray[i1][recipeXMLEmbeddingField],
                        recipeDataArray[i2][recipeXMLEmbeddingField])

            textCosinSim = \
            obj.cos_sim(recipeDataArray[i1][recipePlainTextEmbeddingField],
                        recipeDataArray[i2][recipePlainTextEmbeddingField])

            titleCosinSim = \
            obj.cos_sim(recipeDataArray[i1][recipeTitleEmbeddingField],
                        recipeDataArray[i2][recipeTitleEmbeddingField])

            print('[ m:doc d:' + str(i1) + ', d:' + str(i2) + ' ; m:XMLCosinSim ' + str(XMLCosinSim) + '; ')
            print(' m:textCosinSim ' + str(textCosinSim) + ' ; m:titleCosinSim ' + str(titleCosinSim) + ' ] .')
            i2 += 1
        i1 += 1

