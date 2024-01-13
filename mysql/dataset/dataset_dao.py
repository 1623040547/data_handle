from mysql.dataset.dataset_table import DataSet
from mysql.dataset.daset_data import Sentence


class DataSetDao:
    def __init__(self):
        DataSet.create_dataset_table()
        self.datas = []

    def put(self, sentence: Sentence):
        DataSet.saveSentence(sentence)

    def puts(self, sentences: [Sentence]):
        for sentence in sentences:
            self.put(sentence)

    def save(self):
        DataSet.submit()

    def getSentenceId(self, scene: str, model: str):
        return DataSet.selectSentence(model=model, scene=scene)
