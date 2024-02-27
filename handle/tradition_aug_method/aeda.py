# AEDA: An Easier Data Augmentation Technique for Text classification
# Akbar Karimi, Leonardo Rossi, Andrea Prati

import random

from database.mysql.dataset.daset_data import Scene, Sentence
from database.mysql.dataset.dataset_dao import DataSetDao

PUNCTUATIONS = ['.', ',', '!', '?', ';', ':']


# Insert punction words into a given sentence with the given ratio "punc_ratio"
def insert_punctuation_marks(sentence, punc_ratio=0.3):
    words = sentence.split(' ')
    new_line = []
    q = random.randint(1, int(punc_ratio * len(words) + 1))
    qs = random.sample(range(0, len(words)), q)

    for j, word in enumerate(words):
        if j in qs:
            new_line.append(PUNCTUATIONS[random.randint(0, len(PUNCTUATIONS) - 1)])
            new_line.append(word)
        else:
            new_line.append(word)
    new_line = ' '.join(new_line)
    return new_line


def aeda(sentence,
         punc_ratio=0.3):
    words = sentence.split(' ')
    new_line = []
    q = random.randint(1, int(punc_ratio * len(words) + 1))
    qs = random.sample(range(0, len(words)), q)

    for j, word in enumerate(words):
        if j in qs:
            new_line.append(PUNCTUATIONS[random.randint(0, len(PUNCTUATIONS) - 1)])
            new_line.append(word)
        else:
            new_line.append(word)
    new_line = ' '.join(new_line)
    return new_line


def aeda_gen_data():
    dao = DataSetDao()
    ls = dao.getSentences(scene=Scene.twitter.name, model='')
    # rs = dao.getSentences(scene=Scene.restaurant.name, model='')
    count = 0
    for x in ls:
        print(count)
        count += 1
        for i in range(3):
            s = aeda(x.text)
            dao.put(Sentence(
                scene=x.scene,
                text=s,
                protId=x.sentenceId,
                model='aeda',
                aspect_polarity=x.aspect_polarity,
                prompt=x.prompt,
                promptId=x.promptId,
                protText=x.text,
                sentenceId=0,
            ))
    # for x in rs:
    #     for i in range(4):
    #         s = aeda(x.text)
    #         dao.put(Sentence(
    #             scene=x.scene,
    #             text=s,
    #             protId=x.sentenceId,
    #             model='aeda',
    #             aspect_polarity=x.aspect_polarity,
    #             prompt=x.prompt,
    #             promptId=x.promptId,
    #             protText=x.text,
    #             sentenceId=0,
    #         ))
    dao.save()
