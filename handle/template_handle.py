import random

from data_gen.model.chat import chat
from handle.my_template import MyTemplate
from mysql.dataset.daset_data import Scene, ChatModel
from mysql.dataset.dataset_dao import DataSetDao


class TemplateHandle:
    def __init__(self, scene: Scene, model: ChatModel, template: MyTemplate, batch_size=10, turn=1, retry_time=5):
        self.scene = scene
        self.template = template
        self.batch_size = batch_size
        self.turn = turn
        self.model = model
        self.retry_time = retry_time
        self.dao = DataSetDao()

    def run(self, proto_model: ChatModel):
        for i in [0, self.turn]:
            print('turn: ', i)
            sentences = self.dao.getSentences(self.scene.value.__str__(), proto_model.value.__str__())
            random.shuffle(sentences)
            count = 0
            for j in range(0, int(len(sentences) / self.batch_size + 1)):
                print('step: ', j)
                if count >= len(sentences):
                    break
                print('from: ', count, 'to: ', min(count + self.batch_size, len(sentences)))
                protos = sentences[count: min(count + self.batch_size, len(sentences))]
                text = MyTemplate.genInputText(self.template, protos)
                count += self.batch_size
                for k in range(0, self.retry_time):
                    try:
                        output = chat(self.model, text, self.template)
                        targets = MyTemplate.parseOutputText(self.template, output, protos, self.model.value.__str__())
                        self.dao.puts(targets)
                        self.dao.save()
                        print('save count: ', len(targets))
                        break
                    except:
                        print('retry ... ', k)
