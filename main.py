from xml.dom.minidom import parse
import pymysql

from mysql.dataset_table import DataSet
from mysql.db import Database

dataset_files = {
    'restaurant': './dataset/semeval2014/restaurant/Restaurants_Train.xml',
    'laptop': './dataset/semeval2014/laptop/Laptops_Train.xml'
}

scene = 'laptop'

dom = parse(dataset_files[scene])
# 获取文档元素对象
data = dom.documentElement
# 获取 student
sentences = data.getElementsByTagName('sentence')

DataSet.create_dataset_table()

for sentence in sentences:
    print(sentence)
    text = sentence.getElementsByTagName('text')[0].firstChild.data
    aspect_polarity = []
    for aspectTerm in sentence.getElementsByTagName('aspectTerm'):
        term = aspectTerm.getAttribute('term')
        polarity = aspectTerm.getAttribute('polarity')
        aspect_polarity.append((term,polarity))
    if len(aspect_polarity) != 0:
        DataSet.saveSentence(scene=scene, sentence=text, aspect_polarity=aspect_polarity)
