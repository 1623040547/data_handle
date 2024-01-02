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
    db.create_table(Table.prompt)
    db.create_table(Table.aspect)
    db.create_table(Table.sentence)
    db.create_table(Table.sentence_aspect)


def init_dataset_table():
    if db.table_is_none(TableName.prompt):
        db.insert(first=TableName.prompt + '(`prompt`)', second='\'\'')


init_dataset_table()
