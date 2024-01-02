from xml.dom.minidom import parse
import pymysql

from mysql.db import Database

dataset_files = {
    'restaurant': './dataset/semeval2014/restaurant/Restaurants_Train.xml',
    'laptop': './dataset/semeval2014/laptop/Laptops_Train.xml'
}

dom = parse(dataset_files['laptop'])
# 获取文档元素对象
data = dom.documentElement
# 获取 student
sentences = data.getElementsByTagName('sentence')
sentenceText = data.getElementsByTagName('text')
print(dom)

db = Database()
db.con()





#Rewrite sentences like follows:
#Did not enjoy the new Windows 8 and touchscreen functions. note: Windows 8 is negtive,touchscreen is negtive.
#=>I can't accept this mac as well as the touchscreen functions. note: Mac 8 is negtive,touchscreen is negtive.