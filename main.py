import os
import random
import sys
import threading
from random import shuffle
from threading import Thread
import io

from data_gen.gen import train_for_kgan, deleteCh, train_for_aen_atae
from handle.my_template import MyTemplate
from handle.prot_handle import ProtHandle, DatasetFile
from handle.template_handle import TemplateHandle
from extern_util.interface import ABSAModelArg, KGANModelArg
from mysql.dataset.daset_data import Scene, ChatModel
from mysql.dataset.dataset_dao import DataSetDao

# ProtHandle().parseAndSave(file=DatasetFile.laptop)
# ProtHandle().parseAndSave(file=DatasetFile.restaurant)

# dao = DataSetDao()
# prots = dao.getSentences(scene='laptop', model='')
# train_for_kgan(prots, './tmp.txt')
# arg = KGANModelArg(ds_name=KGANModelArg.ds_name_laptop, dataset_name=KGANModelArg.dataset_name_laptop,
#                    train_file='./tmp.txt')
# arg.run()


def one_thread():
    handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1,
                            turn=1)
    handle.run(proto_model=ChatModel.none)

    handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1,
                            turn=1)
    handle.run(proto_model=ChatModel.none)


for i in range(4):
    one_thread()
