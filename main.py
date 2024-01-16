from handle.my_template import MyTemplate
from handle.template_handle import TemplateHandle
from mysql.dataset.daset_data import Scene, ChatModel

handle = TemplateHandle(scene=Scene.laptop, model=ChatModel.chat_glm_turbo, template=MyTemplate.t1)
handle.run(proto_model=ChatModel.none)
