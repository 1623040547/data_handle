import os
from random import shuffle

import time

import nltk

from database.mysql.dataset.dataset_dao import DataSetDao
from database.mysql.experiment.experiment_dao import ExperimentDao
from database.mysql.experiment.experiment_data import ExperimentCome
from extern_util.interface import ABSAModelRunner
from handle.data_gen.model.chat import chat
from handle.method.bleu_select import bleu_select_sample
from handle.method.random_select import random_select, RandomSelect, random_select_2, random_select_3, \
    random_select_eda, random_select_aeda
from handle.my_template import MyTemplate
from handle.prot_handle import DatasetFile
from handle.template_handle import TemplateHandle
from database.mysql.dataset.daset_data import ChatModel, Scene, Sentence
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from handle.tradition_aug_method.aeda import aeda_gen_data
from handle.tradition_aug_method.eda import eda_gen_data


# def outcome_write_to_db(path: str):
#     for file in os.listdir(path):
#         try:
#             t = float(file.replace('.json', ''))
#             f = path + '\\' + file
#             come = ExperimentCome.fromJson(open(f).read(), tid=t)
#             dao = ExperimentDao()
#             dao.put(come)
#         except:
#             continue
#
#
# def bleu_test():
#     for file in os.listdir(r'C:\Users\16230\PycharmProjects\dataHandle\log\log_mem_bleu_test_rest'):
#         try:
#             t = float(file.replace('.json', ''))
#             f = r'C:\Users\16230\PycharmProjects\dataHandle\log\log_mem_bleu_test_rest' + '\\' + file
#             come = ExperimentCome.fromJson(open(f).read(), tid=t)
#             print(come.method)
#             print('acc: ' + str(come.acc()))
#             print('f1: ' + str(come.f1()))
#             print('best_acc: ' + str(come.best_acc()))
#             print('best_f1: ' + str(come.best_f1()))
#             print()
#             print()
#         except:
#             continue


# eda_gen_data()
#
# aeda_gen_data()

# bleu_test()

# handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1, turn=4)
#
# handle.run()
#
# handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1, turn=4)
#
# handle.run()
#
# handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.llama_70_chat, template=MyTemplate.t1, turn=4)
#
# handle.run()
#
# handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.llama_70_chat, template=MyTemplate.t1, turn=4)
#
# handle.run()
#
# handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_35_turbo, template=MyTemplate.t1, turn=4)
#
# handle.run()
#
# handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.chat_35_turbo, template=MyTemplate.t1, turn=4)
#
# handle.run()


# outcome_write_to_db(r'C:\Users\16230\Desktop\log3')
# outcome_write_to_db(r'C:\Users\16230\PycharmProjects\dataHandle\log')

random_select_eda()

random_select_aeda()
#
# f_rest_n = f_rest_s.read() +

# bleu_test()

# bleu_select_sample()
#
# dao = ExperimentDao()
#
# experiments = dao.getExperiments()
#
# specs = dao.getSpecExperiments(absa_model="atae", chat_model=ChatModel.chat_glm_turbo.name,
#                                method_pattern=RandomSelect.method_1, dataset="restaurant")
#
# for spec in specs:
#     print(spec.method)
#
# print()
#
# for spec in specs:
#     print(spec.acc())
#
# print()
# for spec in specs:
#     print(spec.best_acc())
#
# specs = dao.getSpecExperiments(absa_model="atae", chat_model=ChatModel.chat_glm_turbo.name,
#                                method_pattern=RandomSelect.method_1, dataset="laptop")
#
# print()
# print()
# print()
# print()
# print()
#
# for spec in specs:
#     print(spec.f1())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.acc())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.best_acc())
#
# print()
# print()
# print()
# print()
#
# specs = dao.getSpecExperiments(absa_model="atae", chat_model=ChatModel.chat_glm_turbo.name,
#                                method_pattern=RandomSelect.method_1, dataset="restaurant")
#
# print()
# print()
#
# for spec in specs:
#     print(spec.f1())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.acc())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.best_acc())
#
# print()
# print()
# print()
# print()
#
# specs = dao.getSpecExperiments(absa_model="atae", chat_model=ChatModel.llama_70_chat.name,
#                                method_pattern=RandomSelect.method_1, dataset="restaurant")
#
# print()
# print()
#
# for spec in specs:
#     print(spec.f1())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.acc())
#
# print()
# print()
#
# for spec in specs:
#     print(spec.best_acc())
#
# print()
# print()
