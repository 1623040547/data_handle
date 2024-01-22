import bz2
import json
import zlib
from dataclasses import dataclass

from database.mysql.dataset.daset_data import Sentence


@dataclass()
class ExperimentOne:
    seed: int
    test_acc: float
    test_f1: float
    epoch: int

    def toJson(self):
        jsons = {}
        jsons['seed'] = self.seed
        jsons['test_acc'] = self.test_acc
        jsons['test_f1'] = self.test_f1
        jsons['epoch'] = self.epoch
        return jsons

    @classmethod
    def fromJson(cls, jsons: str):
        jsons = json.loads(jsons)
        return ExperimentOne(
            seed=jsons['seed'],
            test_acc=jsons['test_acc'],
            test_f1=jsons['test_f1'],
            epoch=jsons['epoch'],
        )

    @classmethod
    def fromOutcomes(cls, jsons: str):
        jsons = json.loads(jsons)
        outcomes = []
        for i in jsons:
            out = ExperimentOne(
                seed=i["seed"],
                test_acc=i["test_acc"],
                test_f1=i["test_f1"],
                epoch=i["epoch"],
            )
            outcomes.append(out)
        return outcomes

    @classmethod
    def getIds(cls, sens: list[Sentence]):
        ids = []
        for s in sens:
            ids.append(s.sentenceId)
        return ids


@dataclass()
class ExperimentCome:
    id: str
    absa_model: str  # kgan atae aen
    dataset: str  # laptop restaurant
    learning_rate: float
    dropout_rate: float
    n_epoch: int
    bs: int
    patience: int
    seeds: [int]
    valset_ratio: float
    ids: [int]
    outcomes: list[ExperimentOne]

    def toIds(self):
        source = ','.join([str(x) for x in self.ids])
        ids = bz2.compress(bytes(source, 'utf-8'))
        l = len(ids)
        ids = int.from_bytes(ids, 'big')
        ids = l.__str__() + ' ' + ids.__str__()
        return ids

    @classmethod
    def fromIds(cls, zip_str: str):
        args = zip_str.split(' ')
        zip_str = int.to_bytes(int(args[1]), int(args[0]), 'big')
        decompressed_data = bz2.decompress(zip_str)
        return decompressed_data.decode('utf-8')

    @classmethod
    def fromJson(cls, jsons: str):
        jsons = json.loads(jsons)
        return ExperimentCome(
            id=jsons['id'],
            absa_model=jsons['absa_model'],
            dataset=jsons['dataset'],
            learning_rate=jsons['learning_rate'],
            dropout_rate=jsons['dropout_rate'],
            n_epoch=jsons['n_epoch'],
            bs=jsons['bs'],
            patience=jsons['patience'],
            seeds=jsons['seeds'],
            valset_ratio=jsons['valset_ratio'],
            ids=jsons['ids'],
            outcomes=ExperimentOne.fromOutcomes(json.dumps(jsons['outcomes']))
        )

    def toJson(self):
        jsons = {}
        jsons['absa_model'] = self.absa_model
        jsons['dataset'] = self.dataset
        jsons['learning_rate'] = self.learning_rate
        jsons['dropout_rate'] = self.dropout_rate
        jsons['n_epoch'] = self.n_epoch
        jsons['bs'] = self.bs
        jsons['patience'] = self.patience
        jsons['seeds'] = self.seeds
        jsons['valset_ratio'] = self.valset_ratio
        jsons['ids'] = self.ids
        jsons['outcomes'] = []
        for out in self.outcomes:
            jsons['outcomes'].append(out.toJson())
        return jsons
