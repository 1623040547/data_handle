from database.mysql.dataset.daset_data import Scene, ChatModel
from handle.my_template import MyTemplate
from handle.template_handle import TemplateHandle
from handle.tradition_aug_method.aeda import aeda_gen_data

handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.llama_70_chat, template=MyTemplate.t1, turn=4)

handle.run()

# aeda_gen_data()