from mysql.db import Database

db = Database('dataset')


class TableName:
    sentence = "sentence"
    aspect = "aspect"
    prompt = "prompt"
    sentence_aspect = "laptop_aspect"


class Table:
    sentence = TableName.sentence + """(
    id int(8) primary key auto_increment,
    text varchar(512) unique key,
    scene varchar(256),
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


def create_dataset_table():
    """
    创建用于存储ABSA数据集的关系表格，
    prompt代表生成此条数据所用模板，原始数据无模板，
    sentence为此条数据文本内容，
    aspect代表sentence中所拥有的方面信息，
    sentence_aspect代表aspect在sentence中的情感
    """
    db.create_table(Table.prompt)
    db.create_table(Table.aspect)
    db.create_table(Table.sentence)
    db.create_table(Table.sentence_aspect)
    __init_dataset_table()


def __init_dataset_table():
    if db.table_is_none(TableName.prompt):
        __savePrompt('\'\'')


def promptExist(prompt: str):
    """
    :param prompt: 传入模板
    :return: int: 模板存在则返回模板id，否则返回-1
    """
    rows = db.select(sel='id', table=TableName.prompt, condition='prompt = {0}'.format(prompt))
    if rows.count == 0:
        return -1
    else:
        return rows[0][0]


def aspectExist(aspect: str):
    rows = db.select(sel='id', table=TableName.aspect, condition='aspect = {0}'.format(aspect))
    if rows.count == 0:
        return -1
    else:
        return rows[0][0]


def sentenceExist(sentence: str):
    rows = db.select(sel='id', table=TableName.sentence, condition='sentence = {0}'.format(sentence))
    if rows.count == 0:
        return -1
    else:
        return rows[0][0]


def __savePrompt(prompt: str):
    id = promptExist(prompt)
    if id > -1:
        return id
    else:
        db.insert(table=TableName.prompt + '(`prompt`)', values=prompt)
        return __savePrompt(prompt)


def __saveAspect(aspect: str):
    id = aspectExist(aspect)
    if id > -1:
        return id
    else:
        db.insert(table=TableName.aspect + '(`aspect`)', values=aspect)
        return __saveAspect(aspect)


def __saveSentence(scene: str, sentence: str, promptId: int):
    id = sentenceExist(sentence)
    if id > -1:
        return id
    else:
        db.insert(table=TableName.sentence + '(`text`,`scene`,`promptId`)',
                  values='{0},{1},{2}'.format(sentence, scene, promptId))
        return __saveSentence(scene, sentence, promptId)


def __saveSentenceAspect(polarity: str, sentenceId: int, aspectId: int):
    db.insert(table=TableName.sentence_aspect + '(`polarity`,`sentenceId`,`aspectId`)',
              values='{0},{1},{2}'.format(polarity, sentenceId, aspectId))


def saveSentence(scene: str, sentence: str, aspect_polarity: [(str, str)], prompt=''):
    sentenceId = sentenceExist(sentence)
    if sentenceId > -1:
        return
    promptId = __savePrompt(prompt)
    sentenceId = __saveSentence(scene, sentence, promptId)
    aspectIds = []
    for pair in aspect_polarity:
        aspectId = __saveAspect(pair[0])
        aspectIds.append([aspectId, pair[1]])
    for pair in aspectIds:
        __saveSentenceAspect(
            aspectId=pair[0],
            polarity=pair[1],
            sentenceId=sentenceId,
        )


def saveDb():
    db.save()
