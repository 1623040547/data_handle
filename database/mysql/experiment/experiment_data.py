import bz2
import json
import zlib
from dataclasses import dataclass

import numpy as np

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
    chat_model: str
    dataset: str  # laptop restaurant
    learning_rate: float
    dropout_rate: float
    n_epoch: int
    bs: int
    patience: int
    seeds: [int]
    valset_ratio: float
    ids: [int]
    method: str
    outcomes: list[ExperimentOne]

    def acc(self):
        acc = 0
        for o in self.outcomes:
            acc += o.test_acc
        return acc / len(self.outcomes)

    def f1(self):
        f1 = 0
        for o in self.outcomes:
            f1 += o.test_f1
        return f1 / len(self.outcomes)

    def best_acc(self):
        best_acc = 0
        for o in self.outcomes:
            best_acc = max(best_acc, o.test_acc)
        return best_acc

    def best_f1(self):
        best_f1 = 0
        for o in self.outcomes:
            best_f1 = max(best_f1, o.test_f1)
        return best_f1

    def acc_var(self):
        a = []
        for o in self.outcomes:
            a.append(o.test_acc)
        return np.var(a)

    def f1_var(self):
        a = []
        for o in self.outcomes:
            a.append(o.test_f1)
        return np.var(a)

    def toIds(self):
        source = ','.join([str(x) for x in self.ids])
        ids = bz2.compress(bytes(source, 'utf-8'))
        l = len(ids)
        ids = int.from_bytes(ids, 'big')
        ids = l.__str__() + ' ' + ids.__str__()
        return ids

    @classmethod
    def fromIds(cls, zip_str: bytes):
        return []
        pass
        # args = zip_str.decode('utf-8').split(' ')
        # print(int(args[1]))
        # zip_str = int.to_bytes(int(args[1]), int(args[0]), 'big')
        # decompressed_data = bz2.decompress(zip_str)
        # return [int(x) for x in decompressed_data.decode('utf-8').split(',')]

    @classmethod
    def fromJson(cls, jsons: str, tid: float):
        jsons = json.loads(jsons)
        try:
            print('guideLine: ' + str(jsons['guideLine']))
        except:
            pass
        return ExperimentCome(
            id=str(tid),
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
            outcomes=ExperimentOne.fromOutcomes(json.dumps(jsons['outcomes'])),
            chat_model=jsons['chat_model'],
            method=jsons['method']
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
        jsons['method'] = self.method
        jsons['chat_model'] = self.chat_model
        jsons['outcomes'] = []
        for out in self.outcomes:
            jsons['outcomes'].append(out.toJson())
        return jsons
