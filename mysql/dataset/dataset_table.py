from mysql.dataset.daset_data import Sentence, AspectPolarity
from mysql.db import Database

_db = Database('dataset')


class TableName:
    sentence = "sentence"
    aspect = "aspect"
    prompt = "prompt"
    sentence_aspect = "sentence_aspect"


class Table:
    sentence = TableName.sentence + """(
    id int(8) primary key auto_increment,
    text LONGTEXT,
    scene varchar(256),
    model varchar(64),
    promptId int(8), 
    protId int(8),
    foreign key(promptId) references prompt(id)
    )
"""
    aspect = TableName.aspect + """(
    id int(8) primary key auto_increment,
    aspect varchar(256) unique key
    )
"""
    prompt = TableName.prompt + """(
    id int(8) primary key auto_increment,   
    prompt LONGTEXT
    )
"""
    sentence_aspect = TableName.sentence_aspect + """(
    id int(8) primary key auto_increment,
    sentenceId int(8), 
    aspectId int(8),
    polarity ENUM('positive','negative','neutral'),
    foreign key(sentenceId) references sentence(id),
    foreign key(aspectId) references aspect(id)
    )              
"""


class DataSet:
    __aspectMap = {}

    @classmethod
    def create_dataset_table(cls):
        """
        创建用于存储ABSA数据集的关系表格，
        prompt代表生成此条数据所用模板，原始数据无模板，
        sentence为此条数据文本内容，
        aspect代表sentence中所拥有的方面信息，
        sentence_aspect代表aspect在sentence中的情感
        """
        _db.create_table(Table.prompt)
        _db.create_table(Table.aspect)
        _db.create_table(Table.sentence)
        _db.create_table(Table.sentence_aspect)
        DataSet.__init_dataset_table()

    @classmethod
    def __init_dataset_table(cls):
        if _db.table_is_none(TableName.prompt):
            DataSet.__savePrompt("''")
            DataSet.submit()

    @classmethod
    def promptExist(cls, prompt: str):
        """
        :param prompt: 传入模板
        :return: int: 模板存在则返回模板id，否则返回-1
        """
        rows = _db.select(sel='id', table=TableName.prompt, condition='prompt = \'{0}\''.format(toQuot(prompt)))
        if len(rows) == 0:
            return -1
        else:
            return rows[0][0]

    @classmethod
    def aspectExist(cls, aspect: str):
        rows = _db.select(sel='id', table=TableName.aspect, condition='aspect = \'{0}\''.format(toQuot(aspect)))
        if len(rows) == 0:
            return -1
        else:
            return rows[0][0]

    @classmethod
    def sentenceExist(cls, text: str):
        rows = _db.select(sel='id', table=TableName.sentence, condition='text = \'{0}\''.format(toQuot(text)))
        if len(rows) == 0:
            return -1
        else:
            return rows[0][0]

    @classmethod
    def __savePrompt(cls, prompt: str):
        tid = DataSet.promptExist(prompt)
        if tid > -1:
            return tid
        else:
            _db.insert(table=TableName.prompt + '(`prompt`)', values='\'{0}\''.format(toQuot(prompt)))
            return DataSet.__savePrompt(prompt)

    @classmethod
    def __saveAspect(cls, aspect: str):
        tid = DataSet.aspectExist(aspect)
        if tid > -1:
            return tid
        else:
            _db.insert(table=TableName.aspect + '(`aspect`)', values='\'{0}\''.format(toQuot(aspect)))
            return DataSet.__saveAspect(aspect)

    @classmethod
    def __saveSentence(cls, model: str, scene: str, sentence: str, promptId: int, protId=-1):
        tid = DataSet.sentenceExist(sentence)
        if tid > -1:
            return tid
        else:
            _db.insert(table=TableName.sentence + '(`model`,`text`,`scene`,`promptId`,`protId`)',
                       values='\'{0}\',\'{1}\',\'{2}\',{3},{4}'
                       .format(toQuot(model), toQuot(sentence), toQuot(scene), promptId, protId))
            return DataSet.__saveSentence(model, scene, sentence, promptId)

    @classmethod
    def __saveSentenceAspect(cls, polarity: str, sentenceId: int, aspectId: int):
        return _db.insert(table=TableName.sentence_aspect + '(`polarity`,`sentenceId`,`aspectId`)',
                          values='\'{0}\',{1},{2}'.format(toQuot(polarity), sentenceId, aspectId))

    @classmethod
    def __getAspects(cls):
        if len(cls.__aspectMap) != 0:
            return cls.__aspectMap
        aspects = _db.select(sel='id,aspect', table=TableName.aspect, condition='id > -1')
        for aspect in aspects:
            cls.__aspectMap[aspect[0]] = fromQuot(aspect[1])

    @classmethod
    def selectSentence(cls, model: str, scene: str):
        sentences = []
        datas = _db.select(sel='id,text,promptId,protId', table=TableName.sentence,
                           condition='model = \'{0}\' and scene =\'{1}\''.format(model, scene))
        for data in datas:
            sentence = Sentence.sentence()
            sentence.sentenceId = data[0]
            sentence.text = fromQuot(data[1])
            sentence.promptId = data[2]
            sentence.protId = data[3]
            sentences.append(sentence)

        cls.__getAspects()

        for sentence in sentences:
            datas = _db.select(sel='aspectId,polarity', table=TableName.sentence_aspect,
                               condition='sentenceId = {0}'.format(sentence.sentenceId))
            for data in datas:
                sentence_aspect = AspectPolarity.instance()
                sentence_aspect.aspectId = data[0]
                sentence_aspect.polarity = data[1]
                sentence_aspect.aspect = cls.__aspectMap[data[0]]
                sentence.aspect_polarity.append(sentence_aspect)
        return sentences

    @classmethod
    def saveSentence(cls, sentence: Sentence):
        sentence.sentenceId = DataSet.sentenceExist(sentence.text)
        sentence.promptId = DataSet.promptExist(sentence.prompt)
        sentence.protId = DataSet.sentenceExist(sentence.protText)
        if sentence.sentenceId > -1:
            return
        sentence.promptId = DataSet.__savePrompt(sentence.prompt)
        sentence.sentenceId = DataSet.__saveSentence(sentence.model, sentence.scene, sentence.text, sentence.promptId,
                                                     sentence.protId)
        for item in sentence.aspect_polarity:
            item.aspectId = DataSet.__saveAspect(item.aspect)
            count = DataSet.__saveSentenceAspect(
                aspectId=item.aspectId,
                polarity=item.polarity,
                sentenceId=sentence.sentenceId,
            )
            if count <= 0:
                raise

    @classmethod
    def submit(cls):
        _db.save()


def toQuot(s: str):
    return s.replace('\'', '&apos').replace('"', '&quot')


def fromQuot(s: str):
    return s.replace('&apos', '\'').replace('&quot', '\'')
