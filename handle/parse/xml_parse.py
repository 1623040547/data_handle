from xml.dom.minidom import parse

from database.mysql.dataset.daset_data import Sentence, AspectPolarity, Polarity


class XmlParse:
    @classmethod
    def parse(cls, path: str):
        datas = []
        dom = parse(path)
        data = dom.documentElement
        sentences = data.getElementsByTagName('sentence')
        for sentence in sentences:
            data = Sentence.sentence()
            data.text = sentence.getElementsByTagName('text')[0].firstChild.data
            for aspectTerm in sentence.getElementsByTagName('aspectTerm'):
                term = aspectTerm.getAttribute('term')
                polarity = aspectTerm.getAttribute('polarity')
                if Polarity.contains(polarity):
                    data.aspect_polarity.append(AspectPolarity(
                        aspectId=-1,
                        aspect=term,
                        polarity=polarity
                    ))
            if len(data.aspect_polarity) != 0:
                datas.append(data)
        return datas
