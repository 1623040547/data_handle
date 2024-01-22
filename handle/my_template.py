import re
from enum import Enum

from handle.template_data import template1
from mysql.dataset.daset_data import Sentence
from mysql.dataset.dataset_dao import DataSetDao

_dao = DataSetDao()


class _Count:
    invalidCount = 0
    validCount = 0


class MyTemplate(Enum):
    t1 = template1

    @classmethod
    def genInputText(cls, template: Enum, sentences: list[Sentence]):
        text = ''
        if template == MyTemplate.t1:
            for i, sentence in enumerate(sentences):
                aspects = ''
                for aspect_polarity in sentence.aspect_polarity:
                    aspects += '\'' + aspect_polarity.aspect + '\'' + ','
                aspects = aspects.rstrip(',')
                text += '{0}.{1} {2}\n'.format(i + 1, sentence.text, 'rewrite and include the words ' + aspects + '.')
        return text

    @classmethod
    def parseOutputText(cls, template: Enum, text: str, protos: list[Sentence], model: str):
        sentences = []
        if template == MyTemplate.t1:
            text = text.strip().strip('"').strip().strip("'")
            slices = text.split('\\n')
            count = 0
            for sl in slices:
                if sl.__contains__('{0}.'.format(count + 1)):
                    count += 1
                    try:
                        sl = sl.strip().strip('{0}.'.format(count)).strip("'").strip()
                        proto = protos[count - 1]
                        aspects = proto.getAspects()
                        sentence = MyTemplate.cp_and_save(aspects, sl, proto, model, template)
                        if sentence is not None:
                            sentences.append(sentence)
                    except Exception as e:
                        print(e)
                        print('parse error: ', sl)
        print('total valid: ', _Count.validCount)
        print('total invalid: ', _Count.invalidCount)
        print('valid proportion: ', _Count.validCount / (_Count.invalidCount + _Count.validCount))
        return sentences

    @classmethod
    def cp_and_save(cls, aspects: [str], text: str, proto: Sentence, model: str, template: Enum):
        valid = True
        sentence = Sentence.sentence()
        sentence.text = text
        sentence.scene = proto.scene
        sentence.prompt = template.value.__str__()
        sentence.protId = proto.sentenceId
        sentence.model = model
        sentence.protText = proto.text
        valid &= len(aspects) == len(proto.aspect_polarity)
        for aspect in aspects:
            asp = proto.getAspectPolarity(aspect)
            # 判断方面词与原词是否保持一致
            if asp is not None:
                sentence.aspect_polarity.append(asp)
            else:
                valid &= False
            # 判断方面词石佛还存在于改写文本中
            if not text.lower().__contains__(aspect.lower()):
                valid &= False
        if valid:
            _Count.validCount += 1
            return sentence
        else:
            _dao.putInvalid(sentence, aspects)
            _dao.save()
            _Count.invalidCount += 1
            return None
