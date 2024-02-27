from xml.dom.minidom import parse

from database.mysql.dataset.daset_data import Sentence, AspectPolarity, Polarity

polarity_map = {0: "neutral", 1: "positive", -1: "negative"}


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

    @classmethod
    def parse_twitter(cls, path: str):
        datas = []
        s = open(path, encoding='utf-8').readlines()
        i = int(len(s) / 3) - 1
        data = Sentence.sentence()
        # 0 -> sentence 1 -> aspect 2 -> polarity
        for index in range(i):
            base_index = index * 3
            if data.text == "":
                data.text = s[base_index].replace("$T$", s[base_index + 1].replace('\n', ''))
                data.aspect_polarity.append(AspectPolarity(
                    aspectId=-1,
                    aspect=s[base_index + 1].replace('\n', ''),
                    polarity=polarity_map[int(s[base_index + 2].replace('\n', ''))]
                ))
            elif data.text == s[base_index].replace("$T$", s[base_index + 1].replace('\n', '')):
                data.aspect_polarity.append(AspectPolarity(
                    aspectId=-1,
                    aspect=s[base_index + 1].replace('\n', ''),
                    polarity=polarity_map[int(s[base_index + 2].replace('\n', ''))]
                ))
            else:
                datas.append(data)
                data = Sentence.sentence()
                data.text = s[base_index].replace("$T$", s[base_index + 1].replace('\n', ''))
                data.aspect_polarity.append(AspectPolarity(
                    aspectId=-1,
                    aspect=s[base_index + 1].replace('\n', ''),
                    polarity=polarity_map[int(s[base_index + 2].replace('\n', ''))]
                ))
        datas.append(data)
        return datas
