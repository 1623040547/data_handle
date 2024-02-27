from database.mysql.dataset.daset_data import Scene, ChatModel
from handle.my_template import MyTemplate
from handle.template_handle import TemplateHandle

handle = TemplateHandle(scene=Scene.twitter, model=ChatModel.chat_35_turbo, template=MyTemplate.t1, turn=2)

handle.run()
