import re
from random import shuffle

import nltk

from database.mysql.dataset.daset_data import Sentence, Scene, ChatModel

from nltk.translate.bleu_score import sentence_bleu

from database.mysql.dataset.dataset_dao import DataSetDao
from extern_util.interface import start_experiment_atae, start_experiment_mem


class BleuSelect:
    method_1 = "bleu_select_1_"
    method_1_sample = "bleu_select_1_sample_"

    def __init__(self, sentences: list[Sentence], protos: list[Sentence], step: float, epoch: int, guide_line: float):
        shuffle(sentences)
        self.sentences = sentences
        self.step = step
        self.epoch = epoch
        self.epoch_i = 0
        self.size = len(protos)
        self.map_data = {}
        self.at = 0
        self.map_keys = {0: [], 1: []}
        self.outcomes = []
        self.proto_map = {}
        self.guide_line = guide_line
        for sentence in protos:
            self.proto_map[sentence.sentenceId] = sentence

        for sentence in sentences:
            if self.map_data.__contains__(sentence.protId):
                self.map_data[sentence.protId].append(sentence)
            else:
                self.map_keys[0].append(sentence.protId)
                self.map_data[sentence.protId] = [sentence]

        for k, v in self.map_data.items():
            self.map_data[k] = self.bleu_sort(v, self.proto_map[k].sentenceId)

    def one(self):
        return self.map_keys[self.at]

    def another(self):
        return self.map_keys[(self.at + 1) % 2]

    def forward(self, method: str):
        if self.epoch_i >= self.epoch:
            return False
        self.epoch_i += 1
        self.method_1 = method + str(self.epoch_i * self.step)
        count = int(self.size * self.step)
        shuffle(self.map_keys[0])
        shuffle(self.map_keys[1])
        for i in range(count):
            if len(self.one()) != 0:
                s = self.get_sentence(self.one()[0])
                if s is None:
                    self.one().remove(self.one()[0])
                    count = count + 1
                else:
                    self.another().append(self.one()[0])
                    self.one().remove(self.one()[0])
                    self.outcomes.append(s)
            else:
                self.at = (self.at + 1) % 2
                count = count + 1
        return True

    def get_sentence(self, protId: int):
        if len(self.map_data[protId]) == 0:
            return None
        else:
            s = self.map_data[protId][0]
            self.map_data[protId].remove(s)
            return s

    def bleu_sort(self, sentences: list[Sentence], protId: int):
        reference = nltk.word_tokenize(re.sub(r'[^\w\s]', ' ', self.proto_map[protId].text))
        s = {}
        for sen in sentences:
            candidate = nltk.word_tokenize(re.sub(r'[^\w\s]', ' ', sen.text))
            score = sentence_bleu(reference, candidate)
            v = abs(score)
            print(v)
            s[v] = sen
        ss = [value for key, value in sorted(s.items(), key=lambda item: item[0])]
        index = int(self.guide_line * 10)
        sss = []
        for i in range(len(ss)):
            item = max(min(index, len(ss) - 1), 0)
            sss.append(ss[item])
            ss.remove(ss[item])
        return sss


def bleu_select_sample(step=0.2):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        prot_map = {}
        for p in prot_sentences:
            prot_map[p.sentenceId] = p
        # start_experiment(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=BleuSelect.method_1_sample,
        # )
        aug_sentences = []
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences.extend(dao.getSentences(scene=scene, model=model))
        for s in aug_sentences:
            if len(s.aspect_polarity) == 0:
                s.aspect_polarity = prot_map[s.protId].aspect_polarity
        model = 'complex'
        guideLine = 0
        while guideLine <= 1:
            print("guideLine: " + str(guideLine))
            bleu_sel = BleuSelect(aug_sentences, prot_sentences, 0.25, 2, guideLine)
            while bleu_sel.forward(BleuSelect.method_1_sample):
                start_experiment_atae(
                    scene=scene,
                    sentences=bleu_sel.outcomes,
                    chat_model=model,
                    method=bleu_sel.method_1,
                )
                print("epoch: " + str(bleu_sel.epoch_i))
            guideLine += step


def bleu_select_atae(guide=0.2):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        prot_map = {}
        for p in prot_sentences:
            prot_map[p.sentenceId] = p
        # start_experiment(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=BleuSelect.method_1_sample,
        # )
        aug_sentences = []
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences.extend(dao.getSentences(scene=scene, model=model))
        for s in aug_sentences:
            if len(s.aspect_polarity) == 0:
                s.aspect_polarity = prot_map[s.protId].aspect_polarity
        model = 'complex_' + str(guide)
        guideLine = guide
        print("guideLine: " + str(guideLine))
        bleu_sel = BleuSelect(aug_sentences, prot_sentences, 0.2, 10, guideLine)
        while bleu_sel.forward(BleuSelect.method_1):
            start_experiment_atae(
                scene=scene,
                sentences=bleu_sel.outcomes,
                chat_model=model,
                method=bleu_sel.method_1,
            )
            print("epoch: " + str(bleu_sel.epoch_i))


def bleu_select_mem(guide=0.2):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        prot_map = {}
        for p in prot_sentences:
            prot_map[p.sentenceId] = p
        # start_experiment(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=BleuSelect.method_1_sample,
        # )
        aug_sentences = []
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences.extend(dao.getSentences(scene=scene, model=model))
        for s in aug_sentences:
            if len(s.aspect_polarity) == 0:
                s.aspect_polarity = prot_map[s.protId].aspect_polarity
        model = 'complex_' + str(guide)
        guideLine = guide
        print("guideLine: " + str(guideLine))
        bleu_sel = BleuSelect(aug_sentences, prot_sentences, 0.2, 10, guideLine)
        while bleu_sel.forward(BleuSelect.method_1):
            start_experiment_mem(
                scene=scene,
                sentences=bleu_sel.outcomes,
                chat_model=model,
                method=bleu_sel.method_1,
            )
            print("epoch: " + str(bleu_sel.epoch_i))
