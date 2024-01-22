from handle.data_gen.model.chat_35_turbo import chat_35_turbo
from handle.data_gen.model.chat_glm_turbo import chat_glm_turbo
from handle.data_gen.model.llama_70_chat import Llama
from handle.my_template import MyTemplate
from database.mysql.dataset.daset_data import ChatModel

__l = Llama()


def chat(model: ChatModel, content: str, template: MyTemplate):
    if model.name == ChatModel.chat_35_turbo.name:
        return chat_35_turbo(content, template.value.__str__())
    if model.name == ChatModel.chat_glm_turbo.name:
        return chat_glm_turbo(content, template.value.__str__())
    if model.name == ChatModel.llama_70_chat.name:
        return __l.llama_70_chat(content, template.value.__str__())
