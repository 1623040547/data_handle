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
    text MEDIUMTEXT,
    scene varchar(256),
    model varchar(64),
    promptId int(8), 
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
    prompt MEDIUMTEXT
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
        rows = _db.select(sel='id', table=TableName.prompt, condition='prompt = \'{0}\''.format(prompt))
        if len(rows) == 0:
            return -1
        else:
            return rows[0][0]

    @classmethod
    def aspectExist(cls, aspect: str):
        rows = _db.select(sel='id', table=TableName.aspect, condition='aspect = \'{0}\''.format(aspect))
        if len(rows) == 0:
            return -1
        else:
            return rows[0][0]

    @classmethod
    def sentenceExist(cls, sentence: str):
        rows = _db.select(sel='id', table=TableName.sentence, condition='text = \'{0}\''.format(sentence))
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
            _db.insert(table=TableName.prompt + '(`prompt`)', values='\'{0}\''.format(prompt))
            return DataSet.__savePrompt(prompt)

    @classmethod
    def __saveAspect(cls, aspect: str):
        tid = DataSet.aspectExist(aspect)
        if tid > -1:
            return tid
        else:
            _db.insert(table=TableName.aspect + '(`aspect`)', values='\'{0}\''.format(aspect))
            return DataSet.__saveAspect(aspect)

    @classmethod
    def __saveSentence(cls, model: str, scene: str, sentence: str, promptId: int):
        tid = DataSet.sentenceExist(sentence)
        if tid > -1:
            return tid
        else:
            _db.insert(table=TableName.sentence + '(`model`,`text`,`scene`,`promptId`)',
                       values='\'{0}\',\'{1}\',\'{2}\',{3}'.format(model, sentence, scene, promptId))
            return DataSet.__saveSentence(model, scene, sentence, promptId)

    @classmethod
    def __saveSentenceAspect(cls, polarity: str, sentenceId: int, aspectId: int):
        return _db.insert(table=TableName.sentence_aspect + '(`polarity`,`sentenceId`,`aspectId`)',
                          values='\'{0}\',{1},{2}'.format(polarity, sentenceId, aspectId))

    @classmethod
    def saveSentence(cls, scene: str, sentence: str, aspect_polarity: [(str, str)], prompt='', model=''):
        sentenceId = DataSet.sentenceExist(sentence)
        if sentenceId > -1:
            return
        promptId = DataSet.__savePrompt(prompt)
        sentenceId = DataSet.__saveSentence(model, scene, sentence, promptId)
        aspectIds = []
        for pair in aspect_polarity:
            aspectId = DataSet.__saveAspect(pair[0])
            aspectIds.append([aspectId, pair[1]])
        for pair in aspectIds:
            count = DataSet.__saveSentenceAspect(
                aspectId=pair[0],
                polarity=pair[1],
                sentenceId=sentenceId,
            )
            if count <= 0:
                raise

    @classmethod
    def submit(cls):
        _db.save()
