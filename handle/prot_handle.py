from database.mysql.dataset.dataset_dao import DataSetDao
from handle.parse.xml_parse import XmlParse
from enum import Enum


class DatasetFile(Enum):
    restaurant = './dataset/semeval2014/restaurant/Restaurants_Train.xml'
    laptop = './dataset/semeval2014/laptop/Laptops_Train.xml'
    twitter = r'C:\Users\16230\PycharmProjects\dataHandle\handle\dataset\twitter\train.raw'


class ProtHandle:
    def __init__(self):
        self.dao = DataSetDao()
        self.protDatas = {}

    def parseAndSave(self, file: DatasetFile):
        self.protDatas[file.name] = XmlParse.parse(str(file.value))
        self.setScene(file)
        self.dao.puts(self.protDatas[file.name])
        self.dao.save()

    def parseTwitterAndSave(self, file: DatasetFile):
        self.protDatas[file.name] = XmlParse.parse_twitter(str(file.value))
        self.setScene(file)
        self.dao.puts(self.protDatas[file.name])
        self.dao.save()

    def setScene(self, file: DatasetFile):
        for s in self.protDatas[file.name]:
            s.scene = file.name
