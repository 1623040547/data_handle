from random import shuffle

from database.mysql.dataset.dataset_dao import DataSetDao
from database.mysql.experiment.experiment_dao import ExperimentDao
from database.mysql.experiment.experiment_data import ExperimentCome
from extern_util.interface import ABSAModelRunner
from handle.data_gen.model.chat import chat
from handle.my_template import MyTemplate
from handle.template_handle import TemplateHandle
from database.mysql.dataset.daset_data import ChatModel, Scene, Sentence

json_s = open(r'C:\Users\16230\PycharmProjects\dataHandle\log\1706102828.4258492.json').read()

ExperimentCome = ExperimentCome.fromJson(json_s)

dao = ExperimentDao()
dao.put(ExperimentCome)

#
# ProtHandle().parseAndSave(file=DatasetFile.laptop)
# ProtHandle().parseAndSave(file=DatasetFile.restaurant)
#
# dao = DataSetDao()
# aug = dao.getSentences(scene='laptop', model=ChatModel.chat_glm_turbo.name)
# sel = {}
# for a in aug:
#     if a.promptId == 5:
#         sel[a.protId]=a
# sel_l = list(sel.values())
# out = ABSAModelRunner.for_atae_laptop(sel_l[0:250])
#
# aug = dao.getSentences(scene='restaurant', model=ChatModel.chat_glm_turbo.name)
# shuffle(aug)
# out = ABSAModelRunner.for_atae_rest(aug[0:100])
# print(out)
#
# chat(model=ChatModel.chat_35_turbo, content='hello', template=MyTemplate.t1)


# def one_thread():
#     handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.chat_35_turbo, template=MyTemplate.t1,
#                             turn=1, batch_size=50)
#     handle.run(proto_model=ChatModel.none)
#
#     handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_35_turbo, template=MyTemplate.t1,
#                             turn=1, batch_size=50)
#     handle.run(proto_model=ChatModel.none)
#
#
# def two_thread():
#     handle = TemplateHandle(scene=Scene.restaurant, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1,
#                             turn=1, batch_size=5)
#     handle.run(proto_model=ChatModel.none)
#
#     handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1,
#                             turn=1, batch_size=5)
#     handle.run(proto_model=ChatModel.none)
#
#
# if __name__ == '__main__':
#     for i in range(5):
#         two_thread()
#     for i in range(5):
#         one_thread()
