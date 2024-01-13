import re
from enum import Enum

from handle.template_data import template1
from mysql.dataset.daset_data import Sentence, AspectPolarity


class MyTemplate(Enum):
    t1 = template1

    @classmethod
    def genInputText(cls, template: Enum, sentences: [Sentence]):
        text = ''
        if template == MyTemplate.t1:
            for i, sentence in enumerate(sentences):
                aspects = '['
                for aspect_polarity in sentence.aspect_polarity:
                    aspects += aspect_polarity.aspect + ','
                aspects.rstrip(',')
                aspects += ']'
                text += '{0}.{1} {2}\n'.format(i, aspects, sentence.text)

    @classmethod
    def parseOutputText(cls, template: Enum, text: str, protos: [Sentence]):
        sentences = [Sentence]
        slices = text.split('\n')
        if template == MyTemplate.t1:
            re.fullmatch('[0-9]+\\.[^(\\n)]*\\n',text)
