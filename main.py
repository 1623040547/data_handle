import re
from xml.dom.minidom import parse

from data_gen.model.chat_glm_turbo import chat_glm_turbo
from handle.prot_handle import ProtHandle, DatasetFile
from handle.my_template import MyTemplate
from mysql.dataset.dataset_dao import DataSetDao

# handler = ProtHandle()
#
# handler.parseAndSave(DatasetFile.restaurant)

# data = DataSetDao().getSentenceId(scene='laptop',  model='')
# print(data)

# print(chat_glm_turbo(template=str(MyTemplate.t1.value),
#                      content="""
# 1.[food,kitchen,menu]The food is uniformly exceptional, with a very capable kitchen which will proudly whip up whatever you feel like eating, whether it's on the menu or not.
# 2.[food,perks]Not only was the food outstanding, but the little 'perks' were great.
# 3.[food]Nevertheless the food itself is pretty good.
# 4.[drinks,check]It took half an hour to get our check, which was perfect since we could sit, have drinks and talk!
# """))

text = """
1.[food, kitchen, menu] The cuisine at this establishment is consistently excellent, prepared by a skilled kitchen that gladly creates any dish you desire, regardless of whether it's listed on the menu.\n2.[food, perks] The exceptional food and thoughtful extras made our experience even better.\n3.[food] Despite some concerns, the food served here is genuinely satisfying.\n4.[drinks, check] It took half an hour to receive our bill, which was entirely acceptable as it gave us time to relax, enjoy our beverages, and engage in conversation!
"""

slices = text.split('\n')
for slice in slices:
    if slice.__contains__('1.'):
        aspects = []
        text = ''
        slice = slice.strip('1.')
        fr = re.match(r'\[([^\[|\]]*)]', slice)
        slice = slice.replace(fr.group(), '')
        for aspect in fr.groups()[0].split(','):
            aspect = aspect.strip(' ').rstrip(' ')
            aspects.append(aspect)
            print(aspect)
            print(slice.__contains__(aspect))
