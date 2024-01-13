import os.path

import numpy as np
from scipy import spatial

embeddings_dict = {}

if not os.path.exists('C:/Users/wordsList.npy') & os.path.exists('C:/Users/wordVectors.npy'):
    with open("C:/Users/glove.840B.300d.txt", 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = "".join(values[0:len(values) - 300])
            vector = np.asarray(values[len(values) - 300:], "float32")
            embeddings_dict[word] = vector
    np.save('C:/Users/wordsList', np.array(list(embeddings_dict.keys())))
    np.save('C:/Users/wordVectors', np.array(list(embeddings_dict.values()), dtype='float32'))

wordsList = np.load('C:/Users/wordsList.npy')
wordsList = wordsList.tolist()  # Originally loaded as numpy array
wordVectors = np.load('C:/Users/wordVectors.npy')


class WordDistance:
    @classmethod
    def distance(cls, originWords: list[str], newWords: list[str]):
        arrays = {}
        for originWord in originWords:
            array = []
            for newWord in newWords:
                array.append(WordDistance._distance(originWord, newWord))
            arrays[originWord] = array
        return arrays

    @classmethod
    def _distance(cls, o: str, n: str):
        try:
            return spatial.distance.euclidean(wordVectors[wordsList.index(o)], wordVectors[wordsList.index(n)])
        except:
            return float('inf')


print(WordDistance.distance(['food', 'cookie', 'me'], ['cuisine', 'fool', 'bird']))
