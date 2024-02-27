import re
import nltk
import shutil

from database.mysql.dataset.daset_data import Sentence
from database.mysql.dataset.dataset_dao import DataSetDao
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')


def train_for_aen_atae(sentences: [Sentence], path: str):
    throw_count = 0
    save_count = 0
    train_text = ''
    print('train_for_aen_atae {0}'.format(len(sentences)))
    for sentence in sentences:
        parse_text = parse_word(sentence.text)  # parse_text设定为只读
        if not ['.', '?', '!', ' '].__contains__(parse_text[len(parse_text) - 1]):
            parse_text += ' .'
        for aspect in sentence.aspect_polarity:
            aspect_text = parse_aspect(aspect.aspect.lower())
            my_text = parse_text.lower().replace(' {0}'.format(aspect_text), ' $T$ ').replace(
                '{0} '.format(aspect_text), ' $T$ ')
            train_text = train_text.replace('  ', ' ')
            train_text = train_text.replace('  ', ' ')

            if len(my_text.split('$T$')) == 1:
                if len(aspect_text.split(' ')) != 1:
                    throw_count += 1
                    continue
                my_text, aspect_text = synonyms_replace(my_text, aspect_text)
                if my_text == None:
                    print("throw count " + str(throw_count))
                    throw_count += 1
                    continue

            if len(my_text.split('$T$')) > 2:
                if len(aspect_text.split(' ')) != 1:
                    throw_count += 2
                    continue
                my_text = same_aspect_process(sentence, aspect_text, parse_text)
                if my_text == None:
                    throw_count += 2
                    continue
                train_text += my_text
                save_count += 1
                continue

            save_count += 1
            train_text += my_text.strip() + '\n'
            train_text += aspect_text + '\n'
            train_text += aspect.polarity_int().__str__() + '\n'

    file = open(path, 'w', encoding='utf-8')
    file.write(train_text)
    if len(sentences) == 0:
        return
    print(throw_count)
    print(save_count)
    print('throw count: {0}, save count: {1}, throw ratio: {2}'.format(throw_count, save_count,
                                                                       throw_count / (throw_count + save_count)))
    return throw_count, save_count


def train_for_kgan(sentences: list[Sentence], path: str):
    train_text = ''
    for sentence in sentences:
        parse_text = parse_word(sentence.text)
        if not ['.', '?', '!', ' '].__contains__(parse_text[len(parse_text) - 1]):
            parse_text += ' .'
        for aspect in sentence.aspect_polarity:
            aspect_text = parse_word(aspect.aspect.lower())
            words = parse_word(aspect_text).split(' ')
            new_words = []
            for word in words:
                new_words.append(word + aspect.polarity_tag() + ' ')
            tag_aspect = ' '.join(new_words)
            my_text = parse_text.lower().replace(' {0}'.format(aspect_text), ' {0}'.format(tag_aspect)).replace(
                '{0} '.format(aspect_text), '{0} '.format(tag_aspect)).replace('  ',
                                                                               ' ')
            t = my_text.strip() + '\n'
            train_text += t
    train_text = train_text.strip().rstrip('.\n') + ' .\n'
    train_text = train_text.lower().replace('  ', ' ')
    file = open(path, 'w', encoding='utf-8')
    file.write(train_text)


def count_aspect(text: str, aspect: str):
    return text.count(aspect)


def parse_word(text: str):
    text = ' '.join(nltk.word_tokenize(text))
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
    text = text.replace('-', ' - ')
    text = text.replace(';', ' ; ')
    text = text.replace('  ', ' ')
    text = text.replace('  ', ' ')
    return text


def parse_aspect(text: str):
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
    text = text.replace('-', ' - ')
    text = text.replace(';', ' ; ')
    text = text.replace('  ', ' ')
    text = text.replace('  ', ' ')
    return text


def delete_ch(sentences: list[Sentence]):
    for sentence in sentences:
        if is_ch(sentence.text, sentence.sentenceId):
            sentences.remove(sentence)


def is_ch(text: str, id: int):
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


# 丢弃一个句子中有多个相同的方面
# def twice_filter(sentences: list[Sentence]):
#     for s in sentences:
#         l = []
#         ll = []
#         if s.sentenceId == 1673:
#             print()
#         for asp in s.aspect_polarity:
#             if l.__contains__(asp.aspect.lower()):
#                 ll.append(asp.aspect.lower())
#             else:
#                 l.append(asp.aspect.lower())
#         count = 0
#         for asp in s.aspect_polarity.copy():
#             if ll.__contains__(asp.aspect.lower()):
#                 s.aspect_polarity.remove(asp)
#                 print('dup remove {0}'.format(count))
#                 count = (count + 1) % 2
#         if count != 0:
#             raise

def same_aspect_process(sentence: Sentence, aspect: str, text: str):
    skip = 0
    out = ""
    for s in sentence.aspect_polarity:
        if s.aspect.lower() == aspect.lower():
            text, aspect = synonyms_replace_skip(text=text, aspect=aspect, skip=skip)
            if text == None:
                return None
            out += text.replace('  ', ' ').strip() + '\n'
            out += aspect + '\n'
            out += s.polarity_int().__str__() + '\n'
            skip += 1
    return out


def synonyms_replace(text: str, aspect: str):
    for word in text.split(' '):
        if are_synonyms(word, aspect):
            return text.replace(' ' + word, '$T$').replace(word + ' ', '$T$'), word
    return None, None


def synonyms_replace_skip(text: str, aspect: str, skip: int):
    s = 0
    end = False
    l = []
    for word in text.split(' '):
        if (not end) & are_synonyms(word, aspect):
            if s != skip:
                s += 1
                l.append(word)
                continue
            aspect = word
            l.append('$T$')
            end = True
        else:
            l.append(word)
    if end:
        return ' '.join(l), aspect
    else:
        return None, None


def synonyms_replace_kgan(text: str, aspect: str):
    for word in text.split(' '):
        if are_synonyms(word, aspect):
            return text.replace(word, '$T$', 1), word
    return None, None


synonyms_dict = {}


def are_synonyms(word1, word2):
    if synonyms_dict.__contains__(word1 + word2):
        return synonyms_dict[word1 + word2]

    # 获取单词的词义
    syn1 = wordnet.synsets(word1)
    syn2 = wordnet.synsets(word2)

    # 如果两个单词至少有一个词义，且它们共享一个共同的词义
    if syn1 and syn2:
        for s1 in syn1:
            for s2 in syn2:
                if s1.wup_similarity(s2) > 0.95:  # 使用Wu-Palmer相似度阈值判断
                    synonyms_dict[word1 + word2] = True
                    synonyms_dict[word2 + word1] = True
                    return True
    synonyms_dict[word1 + word2] = False
    synonyms_dict[word2 + word1] = False
    return False
