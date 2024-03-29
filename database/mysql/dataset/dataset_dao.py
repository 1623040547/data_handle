from database.mysql.dataset.dataset_table import DataSet
from database.mysql.dataset.daset_data import Sentence


class DataSetDao:
    def __init__(self):
        DataSet.create_dataset_table()
        self.datas = []

    def put(self, sentence: Sentence):
        DataSet.saveSentence(sentence)

    def puts(self, sentences: [Sentence]):
        count = 0
        for sentence in sentences:
            count += 1
            self.put(sentence)

    def putInvalid(self, sentence: Sentence, aspects: [str]):
        DataSet.saveInvalidSentence(sentence, aspects)

    def save(self):
        DataSet.submit()

    def delete(self, sentenceId: int):
        DataSet.deleteSentence(sentenceId)

    def getSentences(self, scene: str, model: str):
        sens = DataSet.selectSentence(model=model, scene=scene)
        from extern_util.train_data_gen import delete_ch
        delete_ch(sens)
        # twice_filter(sens)
        return sens
