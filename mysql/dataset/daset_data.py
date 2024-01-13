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