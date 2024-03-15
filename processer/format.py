import time
from typing import List

from database.mysql.dataset.daset_data import Sentence, AspectPolarity, ChatModel
import nltk
from nltk.corpus import wordnet

from database.mysql.dataset.dataset_dao import DataSetDao

nltk.download('punkt')
nltk.download('wordnet')

signs = [
    '.',
    '\'',
    '"',
    '?',
    ',',
    '!',
    ':',
    '(',
    ')',
    '[',
    ']',
    '-',
    ';',
    '{',
    '}'
]

tmp = Sentence.sentence()
tmp.text = ("servers tend to overlook drinks, and food portions are too small, "
            "making it difficult for two people to share one entree. "
            "[waiters: negative][FOOD PORTIONS: negative][drinks: neutral][entree: negative]")

tmp.aspect_polarity.append(AspectPolarity(
    aspectId=-1,
    aspect='waiters',
    polarity='negative',
))

tmp.aspect_polarity.append(AspectPolarity(
    aspectId=-1,
    aspect='FOOD PORTIONS',
    polarity='negative',
))

tmp.aspect_polarity.append(AspectPolarity(
    aspectId=-1,
    aspect='drinks',
    polarity='neutral',
))

tmp.aspect_polarity.append(AspectPolarity(
    aspectId=-1,
    aspect='entree',
    polarity='negative',
))


class SentenceFormatter:
    count = 0
    loss_count = 0

    def closeMatch(self, s: Sentence) -> List[Sentence]:
        self._removeTail(s)
        self._textReplaceSign(s)
        return self._closeMatch(s)

    def _closeMatch(self, s: Sentence) -> List[Sentence]:
        ss = []
        text = s.text
        slices = text.split(' ')
        slice_map = {}
        slice_no_sign = []
        for i, t in enumerate(slices):
            slice_map[i] = t
            if not signs.__contains__(t):
                slice_no_sign.append(i)

        # 计算方面词在文本中最匹配的词组，获取方面词的[去标点长度,去标点句子中偏移,最大相似度]
        aspect_offset = {}
        for a in s.aspect_polarity:
            # 方面词获取
            aspect = SentenceFormatter.replaceSign(a.aspect)
            aspects = []
            for b in aspect.split(' '):
                if not signs.__contains__(b):
                    aspects.append(b)

            # 计算与方面词最相近的文本
            start = -1
            if aspect_offset.__contains__(a.aspect.lower()):
                SentenceFormatter.loss_count += 1
                print('duplicate text {0} {1}'.format(a.aspect.lower(), s.text))
                print(s.aspect_polarity)
                print()
                continue
                # start = aspect_offset[a.aspect][1]

            for i, t in enumerate(range(len(slice_no_sign) - len(aspects) + 1)):
                if i <= start:
                    continue
                texts = [slice_map[x] for x in slice_no_sign[i:i + len(aspects)]]
                similarity = 1
                for ii, _ in enumerate(aspects):
                    part_text = str(texts[ii]).lower()
                    part_aspect = str(aspects[ii]).lower()
                    if part_text.__contains__(part_aspect) or part_aspect.__contains__(part_text):
                        similarity &= 1
                    else:
                        similarity = 0
                        continue
                if similarity == 1:
                    offset = slice_no_sign[i]
                    aspect_offset[a.aspect.lower()] = [len(aspects), offset, similarity]
                    break
                else:
                    aspect_offset[a.aspect.lower()] = [len(aspects), 0, similarity]
                    continue

        for a in s.aspect_polarity:
            try:
                if aspect_offset[a.aspect.lower()][2] == 0:
                    print('loss {0} {1}'.format(a.aspect.lower(), s.text))
                    print(s.aspect_polarity)
                    print()
                    SentenceFormatter.loss_count += 1
                    continue
                else:
                    SentenceFormatter.count += 1

                begin = aspect_offset[a.aspect.lower()][1]
                end = aspect_offset[a.aspect.lower()][1] + aspect_offset[a.aspect.lower()][0]
                new_arrays = []
                for i, sl in enumerate(slices):
                    if i == begin:
                        new_arrays.append('$T$')
                    if i < begin or i >= end:
                        new_arrays.append(sl)
                text = ' '.join(new_arrays)
                new_sentence = s.copy_from_aspectId(a.aspectId)
                new_sentence.text = text
                ss.append(new_sentence)
            except:
                SentenceFormatter.loss_count += 1
                print(s.text)
                print(a.aspect)
                print(aspect_offset)
        return ss

    def max_similarity(self, syn1, syn2):
        s = 0
        count = 0
        if syn1 and syn2:
            for s1 in syn1:
                for s2 in syn2:
                    s += s1.wup_similarity(s2)
                    count += 1
        if count == 0:
            return 0
        return s / count

    def _textReplaceSign(self, s: Sentence):
        text = s.text
        text = SentenceFormatter.replaceSign(text)
        if not signs.__contains__(text[-1]):
            text += ' .'
        s.text = text

    # template最后有给二元组，部分返回数据会在输出中带上这个二元组，需要移除
    def _removeTail(self, s: Sentence):
        slices = reversed(s.text)
        left_bracket = '['
        right_bracket = ']'
        forehead = ''
        state = 0
        for slice in slices:
            if slice == right_bracket and state == 0:
                forehead = slice
                state += 1
            elif slice == left_bracket and state == 1:
                forehead = ''
                state = 0
            else:
                forehead += slice
        s.text = ''.join(reversed(forehead))

    @classmethod
    def replaceSign(cls, text: str) -> str:
        for sign in signs:
            text = text.replace(sign, ' {0} '.format(sign))
        text_len = 0
        while text_len != len(text):
            text_len = len(text)
            text = text.replace('  ', ' ')
        return text.strip()
