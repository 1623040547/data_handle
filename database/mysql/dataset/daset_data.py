from dataclasses import dataclass
from enum import Enum


@dataclass
class AspectPolarity:
    aspectId: int
    aspect: str
    polarity: str

    @classmethod
    def instance(cls):
        return AspectPolarity(
            aspectId=-1,
            aspect='',
            polarity='positive',
        )

    def polarity_int(self):
        if self.polarity == Polarity.positive.name.__str__():
            return Polarity.positive.value
        if self.polarity == Polarity.negative.name.__str__():
            return Polarity.negative.value
        if self.polarity == Polarity.neutral.name.__str__():
            return Polarity.neutral.value

    def polarity_tag(self):
        if self.polarity == Polarity.positive.name.__str__():
            return '/p'
        if self.polarity == Polarity.negative.name.__str__():
            return '/n'
        if self.polarity == Polarity.neutral.name.__str__():
            return '/0'


@dataclass
class Sentence:
    scene: str
    text: str
    prompt: str
    model: str
    protText: str
    aspect_polarity: list[AspectPolarity]
    sentenceId: int
    promptId: int
    protId: int

    def getAspectPolarity(self, aspect: str):
        for aspect_p in self.aspect_polarity:
            if aspect_p.aspect.lower() == aspect.lower():
                return aspect_p

    def getAspects(self):
        asp = []
        for aspect_p in self.aspect_polarity:
            asp.append(aspect_p.aspect)
        return asp




    @classmethod
    def sentence(cls):
        return Sentence(
            scene='', text='', prompt='',
            model='', protText='', aspect_polarity=[],
            sentenceId=-1, promptId=-1, protId=-1,
        )


class Polarity(Enum):
    positive = 1
    negative = -1
    neutral = 0

    @classmethod
    def contains(cls, p: str):
        try:
            Polarity.__getitem__(p)
            return True
        except:
            return False


class Scene(Enum):
    restaurant = 'restaurant'
    laptop = 'laptop'


class ChatModel(Enum):
    chat_35_turbo = 'chat_35_turbo'
    chat_glm_turbo = 'chat_glm_turbo'
    llama_70_chat = 'llama_70_chat'
