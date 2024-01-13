from handle.my_template import MyTemplate
from mysql.dataset.daset_data import Sentence


class TemplateHandle:
    def __init__(self, scene: str, model: str, template: MyTemplate, batch_size=10, turn=1, retry_time=5):
        self.scene = scene
        self.template = template
        self.batch_size = batch_size
        self.turn = turn
        self.model = model
        self.retry_time = retry_time


    def genInputText(sentences: [Sentence]):
        pass
