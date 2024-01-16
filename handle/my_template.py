import re
from enum import Enum

from handle.template_data import template1
from mysql.dataset.daset_data import Sentence, AspectPolarity


class MyTemplate(Enum):
    t1 = template1

    @classmethod
    def genInputText(cls, template: Enum, sentences: list[Sentence]):
        text = ''
        if template == MyTemplate.t1:
            for i, sentence in enumerate(sentences):
                aspects = '['
                for aspect_polarity in sentence.aspect_polarity:
                    aspects += aspect_polarity.aspect + ','
                aspects = aspects.rstrip(',')
                aspects += ']'
                text += '{0}.{1} {2}\n'.format(i + 1, aspects, sentence.text)
        return text

    @classmethod
    def parseOutputText(cls, template: Enum, text: str, protos: list[Sentence], model: str):
        sentences = []
        if template == MyTemplate.t1:
            text = text.strip().strip('"').strip().strip("'")
            slices = text.split('\\n')
            count = 0
            invalidCount = 0
            for sl in slices:
                if sl.__contains__('{0}.'.format(count + 1)):
                    count += 1
                    try:
                        aspects = []
                        valid = True
                        sl = sl.strip().strip('{0}.'.format(count))
                        fr = re.match(r'\[([^\[|\]]*)]', sl)
                        sl = sl.replace(fr.group(), '')
                        for aspect in fr.groups()[0].split(','):
                            aspect = aspect.strip()
                            aspects.append(aspect)
                        proto = protos[count - 1]
                        sentence = Sentence.sentence()
                        sentence.text = sl
                        sentence.scene = proto.scene
                        sentence.prompt = template.value.__str__()
                        sentence.protId = proto.sentenceId
                        sentence.model = model
                        sentence.protText = proto.text
                        valid &= len(aspects) == len(proto.aspect_polarity)
                        for aspect in aspects:
                            asp = proto.getAspectPolarity(aspect)
                            if asp is not None:
                                sentence.aspect_polarity.append(asp)
                            else:
                                valid &= False
                        if valid:
                            sentences.append(sentence)
                        else:
                            invalidCount += 1
                            print(sentence.text + " is not valid")
                    except:
                        print('parse error: ', sl)

            print('invalid count: ' + str(invalidCount))
            return sentences
