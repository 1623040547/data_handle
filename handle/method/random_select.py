from random import shuffle

from database.mysql.dataset.daset_data import Sentence, ChatModel, Scene
from database.mysql.dataset.dataset_dao import DataSetDao
from extern_util.interface import start_experiment_atae, start_experiment_mem
from handle.prot_handle import DatasetFile


class RandomSelect:
    # 1:继承随机
    # 2:调整了训练集生成的分词逻辑,改变随机策略，下一次随机句子不继承上一次,增加轮数到10轮，atae调整轮数至25轮,因为数据没加上需要重跑
    # 3:全随机
    method_1 = 'random_select_1_'
    method_2 = 'random_select_2_'
    method_3 = 'random_select_3_'

    def __init__(self, sentences: list[Sentence], original_size: int, step: float, epoch: int):
        shuffle(sentences)
        self.sentences = sentences
        self.step = step
        self.epoch = epoch
        self.epoch_i = 0
        self.size = original_size
        self.map_data = {}
        self.at = 0
        self.map_keys = {0: [], 1: []}
        self.outcomes = []
        for sentence in sentences:
            if self.map_data.__contains__(sentence.protId):
                self.map_data[sentence.protId].append(sentence)
            else:
                self.map_keys[0].append(sentence.protId)
                self.map_data[sentence.protId] = [sentence]

    def one(self):
        return self.map_keys[self.at]

    def another(self):
        return self.map_keys[(self.at + 1) % 2]

    # 继承上一次的随机shujiu
    def forward(self):
        if self.epoch_i >= self.epoch:
            return False
        self.epoch_i += 1
        self.method_1 = RandomSelect.method_1 + str(self.epoch_i * self.step)
        count = int(self.size * self.step)
        shuffle(self.map_keys[0])
        shuffle(self.map_keys[1])
        for i in range(count):
            if len(self.one()) != 0:
                s = self.getSentence(self.one()[0])
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

    # 不继承上一次随机数据
    def forward_2(self):
        if self.epoch_i >= self.epoch:
            return False
        self.epoch_i += 1
        self.method_2 = RandomSelect.method_2 + str(self.epoch_i * self.step)
        self.map_init()
        shuffle(self.map_keys[0])
        shuffle(self.map_keys[1])
        count = int(self.size * self.step)
        for i in range(count * self.epoch_i):
            if len(self.one()) != 0:
                s = self.getSentence(self.one()[0])
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

    def forward_3(self):
        if self.epoch_i >= self.epoch:
            return False
        shuffle(self.sentences)
        self.epoch_i += 1
        self.method_3 = RandomSelect.method_3 + str(self.epoch_i * self.step)
        count = int(self.size * self.step * self.epoch_i)
        self.outcomes = self.sentences[0:count]
        return True

    def map_init(self):
        self.map_data = {}
        self.map_keys = {0: [], 1: []}
        self.outcomes = []
        for sentence in self.sentences:
            if self.map_data.__contains__(sentence.protId):
                self.map_data[sentence.protId].append(sentence)
            else:
                self.map_keys[0].append(sentence.protId)
                self.map_data[sentence.protId] = [sentence]

    def getSentence(self, protId: int):
        if len(self.map_data[protId]) == 0:
            return None
        else:
            s = self.map_data[protId][0]
            self.map_data[protId].remove(s)
            return s


##随机继承混入
def random_select(step=0.25, epoch=10):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        if scene == Scene.twitter.value:
            step = 0.2
        prot_sentences = dao.getSentences(scene=scene, model="")
        # start_experiment_atae(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=RandomSelect.method_1,
        # )
        prot_map = {}
        for prot in prot_sentences:
            prot_map[prot.sentenceId] = prot
        aug_all = []
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences = dao.getSentences(scene=scene, model=model)
            for s in aug_sentences:
                try:
                    if len(s.aspect_polarity) == 0:
                        s.aspect_polarity = prot_map[s.protId].aspect_polarity
                except:
                    pass
            aug_all.extend(aug_sentences)
        print("random_select {0}".format(len(aug_all)))
        ram_sel = RandomSelect(aug_all, len(prot_sentences), step, epoch)
        while ram_sel.forward():
            print("random_select forward {0}".format(len(ram_sel.outcomes)))
            start_experiment_atae(
                scene=scene,
                sentences=ram_sel.outcomes,
                chat_model='complex',
                method=ram_sel.method_1,
            )


def random_select_mem(step=0.25, epoch=10):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        if scene == Scene.twitter.value:
            step = 0.2
        prot_sentences = dao.getSentences(scene=scene, model="")
        # start_experiment_mem(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=RandomSelect.method_1,
        # )
        prot_map = {}
        for prot in prot_sentences:
            prot_map[prot.sentenceId] = prot
        aug_all = []
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences = dao.getSentences(scene=scene, model=model)
            for s in aug_sentences:
                try:
                    if len(s.aspect_polarity) == 0:
                        s.aspect_polarity = prot_map[s.protId].aspect_polarity
                except:
                    pass
            aug_all.extend(aug_sentences)
        print("random_select {0}".format(len(aug_all)))
        ram_sel = RandomSelect(aug_all, len(prot_sentences), step, epoch)
        while ram_sel.forward_2():
            print("random_select forward {0}".format(len(ram_sel.outcomes)))
            start_experiment_mem(
                scene=scene,
                sentences=ram_sel.outcomes,
                chat_model='complex',
                method=ram_sel.method_2,
            )


def random_select_eda(step=0.25, epoch=10):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        # start_experiment(
        #     scene=scene,
        #     sentences=[],
        #     chat_model="",
        #     method=RandomSelect.method_1,
        # )
        prot_map = {}
        for p in prot_sentences:
            prot_map[p.sentenceId] = p
        model = "eda"
        aug_sentences = dao.getSentences(scene=scene, model=model)
        for s in aug_sentences:
            if len(s.aspect_polarity) == 0:
                s.aspect_polarity = prot_map[s.protId].aspect_polarity
        ram_sel = RandomSelect(aug_sentences, len(prot_sentences), step, epoch)
        while ram_sel.forward():
            start_experiment_mem(
                scene=scene,
                sentences=ram_sel.outcomes,
                chat_model=model,
                method=ram_sel.method_1,
            )


def random_select_aeda(step=0.25, epoch=10):
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
        #     method=RandomSelect.method_1,
        # )
        model = "aeda"
        aug_sentences = dao.getSentences(scene=scene, model=model)
        for s in aug_sentences:
            if len(s.aspect_polarity) == 0:
                s.aspect_polarity = prot_map[s.protId].aspect_polarity
        ram_sel = RandomSelect(aug_sentences, len(prot_sentences), step, epoch)
        while ram_sel.forward():
            start_experiment_mem(
                scene=scene,
                sentences=ram_sel.outcomes,
                chat_model=model,
                method=ram_sel.method_1,
            )


###随机不继承混入
def random_select_2(step=0.25, epoch=8):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        start_experiment_atae(
            scene=scene,
            sentences=[],
            chat_model="",
            method=RandomSelect.method_2,
        )
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences = dao.getSentences(scene=scene, model=model)
            ram_sel = RandomSelect(aug_sentences, len(prot_sentences), step, epoch)
            while ram_sel.forward_2():
                print('sentence count: {0}'.format(len(ram_sel.outcomes)))
                start_experiment_atae(
                    scene=scene,
                    sentences=ram_sel.outcomes,
                    chat_model=model,
                    method=ram_sel.method_2,
                )


###全随机混入
def random_select_3(step=0.25, epoch=8):
    dao = DataSetDao()
    for di, de in enumerate(Scene):
        scene = de.value
        prot_sentences = dao.getSentences(scene=scene, model="")
        start_experiment_atae(
            scene=scene,
            sentences=[],
            chat_model="",
            method=RandomSelect.method_3,
        )
        for ci, ce in enumerate(ChatModel):
            model = ce.value
            aug_sentences = dao.getSentences(scene=scene, model=model)
            ram_sel = RandomSelect(aug_sentences, len(prot_sentences), step, epoch)
            while ram_sel.forward_3():
                print('sentence count: {0}'.format(len(ram_sel.outcomes)))
                start_experiment_atae(
                    scene=scene,
                    sentences=ram_sel.outcomes,
                    chat_model=model,
                    method=ram_sel.method_3,
                )
