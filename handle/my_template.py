from enum import Enum

from handle.template_data import template1, template2
from database.mysql.dataset.daset_data import Sentence, AspectPolarity
from database.mysql.dataset.dataset_dao import DataSetDao


class _Count:
    invalidCount = 0
    validCount = 0


class MyTemplate(Enum):
    t1 = template1
    t2 = template2

    @classmethod
    def genInputText(cls, template: Enum, sentences: list[Sentence]):
        text = ''
        count = 0
        if template == MyTemplate.t1:
            for i, sentence in enumerate(sentences):
                for aspect_polarity in sentence.aspect_polarity:
                    aspects = aspect_polarity.aspect
                    text += '{0}.{1} {2}\n'.format(count + 1, sentence.text,
                                                   '   rewrite and include the words ' + aspects + '.')
                    count += 1
        return text

    @classmethod
    def parseOutputText(cls, template: Enum, text: str, protos: list[Sentence], model: str):
        sentences = []
        if template == MyTemplate.t1:
            text = text.strip().strip('"').strip().strip("'")
            if text.__contains__('\\n'):
                slices = text.split('\\n')
            elif text.__contains__('\n'):
                slices = text.split('\n')

            ###记录各方面词
            count = 0
            aspects = []

            ###记录方面词对应原句子
            keys = 0
            keys_protos = {}
            for a in protos:
                aspects.extend(a.getAspects())
                for b in a.getAspects():
                    keys_protos[keys] = a
                    keys += 1

            for sl in slices:
                if sl.__contains__('{0}.'.format(count + 1)):
                    count += 1
                    try:
                        sl = sl.strip().strip('{0}.'.format(count)).strip("'").strip()
                        proto = keys_protos[count - 1]
                        sentence = MyTemplate.cp_and_save(aspects[count - 1], sl, proto, model, template)
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
    def cp_and_save(cls, aspects: str, text: str, proto: Sentence, model: str, template: Enum):
        valid = True
        sentence = Sentence.sentence()
        sentence.text = text
        sentence.scene = proto.scene
        sentence.prompt = template.value.__str__()
        sentence.protId = proto.sentenceId
        sentence.model = model
        sentence.protText = proto.text
        sentence.aspect_polarity = [proto.getAspectPolarity(aspects)]
        if valid:
            _Count.validCount += 1
            return sentence
        else:
            _dao = DataSetDao()
            _dao.putInvalid(sentence, aspects)
            _dao.save()
            _Count.invalidCount += 1
            return None
