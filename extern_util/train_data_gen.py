import re

from database.mysql.dataset.daset_data import Sentence
from database.mysql.dataset.dataset_dao import DataSetDao


def train_for_aen_atae(sentences: [Sentence], path: str):
    train_text = ''
    for sentence in sentences:
        for aspect in sentence.aspect_polarity:
            train_text += sentence.text.replace(aspect.aspect, '$T$').strip() + '\n'
            train_text += aspect.aspect + '\n'
            train_text += aspect.polarity_int().__str__() + '\n'
    file = open(path, 'w', encoding='utf-8')
    train_text = train_text.replace('\xa0', ' ')
    file.write(train_text)


def train_for_kgan(sentences: list[Sentence], path: str):
    train_text = ''
    for sentence in sentences:
        for aspect in sentence.aspect_polarity:
            words = parse_word(aspect.aspect).split(' ')
            new_words = []
            for word in words:
                new_words.append(word + aspect.polarity_tag() + ' ')
            tag_aspect = ' '.join(new_words)
            t = sentence.text.replace(aspect.aspect, tag_aspect).strip() + '\n'
            train_text += t
    train_text = train_text.strip().rstrip('.\n') + ' .\n'
    train_text = train_text.lower().replace('  ', ' ')
    file = open(path, 'w', encoding='utf-8')
    train_text = train_text.replace('\xa0', ' ')
    train_text = parse_word(train_text)
    train_text = train_text.replace(' /p', '/p')
    train_text = train_text.replace(' /n', '/n')
    train_text = train_text.replace(' /0', '/0')
    train_text = train_text.replace('/p/p', '/p')
    train_text = train_text.replace('/0/0', '/0')
    train_text = train_text.replace('/n/n', '/n')
    file.write(train_text)


def parse_word(text: str):
    text = text.replace('.', ' .')
    text = text.replace('\'', ' \' ')
    text = text.replace('"', ' " ')
    text = text.replace('?', ' ?')
    text = text.replace(',', ' ,')
    text = text.replace('!', ' !')
    text = text.replace(':', ' :')
    text = text.replace('(', '( ')
    text = text.replace(')', ' )')
    text = text.replace('[', '[ ')
    text = text.replace(']', ' ]')
    # text = text.replace('-', ' - ')
    text = text.replace(';', ' ; ')
    text = text.replace('  ', ' ')
    return text


def deleteCh(sentences: list[Sentence]):
    for sentence in sentences:
        if isCh(sentence.text, sentence.sentenceId):
            sentences.remove(sentence)


def isCh(text: str, id: int):
    for char in text:
        if is_chinese(char):
            dao = DataSetDao()
            dao.delete(id)
            dao.save()
            print('delete: ', id)
            return True
    return False


# 判断字符是否为汉字
def is_chinese(word):
    if u'\u4e00' <= word <= u'\u9fff':
        return True
    punctuation = """！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)
    if re.match(re_punctuation, word):
        return True
    return False
