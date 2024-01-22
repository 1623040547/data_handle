import time
import json

from database.mysql.experiment.experiment_data import ExperimentOne, ExperimentCome
from extern_util.train_data_gen import train_for_kgan, train_for_aen_atae
from extern_util.absa_arg import KGANModelArg, ABSAModelArg
from database.mysql.dataset.daset_data import Sentence


class ABSAModelRunner:
    @classmethod
    def for_kgan_laptop(cls, aug_sentences=None):
        if aug_sentences is None:
            aug_sentences = []
        train_for_kgan(aug_sentences, './tmp/tmp.txt')
        arg = KGANModelArg(
            ds_name=KGANModelArg.ds_name_laptop,
            dataset_name=KGANModelArg.dataset_name_laptop,
            train_file='./tmp/tmp.txt',
            learning_rate=0.001,
            dropout_rate=0.5,
            n_epoch=20,
            bs=32,
            seeds=[14, 131, 137, 257, 511]
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='kgan',
            dataset='laptop',
            learning_rate=arg.learning_rate,
            dropout_rate=arg.dropout_rate,
            n_epoch=arg.n_epoch,
            bs=arg.bs,
            patience=-1,
            seeds=arg.seeds,
            valset_ratio=0,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))

    @classmethod
    def for_kgan_rest(cls, aug_sentences=None):
        if aug_sentences is None:
            aug_sentences = []
        train_for_kgan(aug_sentences, './tmp/tmp.txt')
        arg = KGANModelArg(
            ds_name=KGANModelArg.ds_name_rest,
            dataset_name=KGANModelArg.dataset_name_rest,
            train_file='./tmp/tmp.txt',
            learning_rate=0.001,
            dropout_rate=0.5,
            n_epoch=20,
            bs=64,
            seeds=[14, 131, 137, 257, 511]
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='kgan',
            dataset='restaurant',
            learning_rate=arg.learning_rate,
            dropout_rate=arg.dropout_rate,
            n_epoch=arg.n_epoch,
            bs=arg.bs,
            patience=-1,
            seeds=arg.seeds,
            valset_ratio=0,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))

    @classmethod
    def for_atae_laptop(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.atae_lstm_command,
            dataset='laptop',
            lr=0.0011,
            dropout=0.5,
            num_epoch=30,
            batch_size=32,
            patience=5,
            seeds=[131, 137, 257, 511, 1013],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='atae',
            dataset='laptop',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))

    @classmethod
    def for_atae_rest(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.atae_lstm_command,
            dataset='restaurant',
            lr=0.0012,
            dropout=0.55,
            num_epoch=30,
            batch_size=64,
            patience=5,
            seeds=[131, 137, 257, 511, 1013],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='atae',
            dataset='restaurant',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))

    @classmethod
    def for_bert_laptop(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.aen_bert_command,
            dataset='laptop',
            lr=5e-5,
            dropout=0.5,
            num_epoch=15,
            batch_size=32,
            patience=5,
            seeds=[511],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='bert',
            dataset='laptop',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))

    @classmethod
    def for_bert_rest(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.aen_bert_command,
            dataset='restaurant',
            lr=5e-5,
            dropout=0.5,
            num_epoch=15,
            batch_size=32,
            patience=5,
            seeds=[511],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='bert',
            dataset='restaurant',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences)
        ))


def saveExperiment(out: ExperimentCome):
    time_s = time.time().__str__()
    open(r'C:\Users\16230\PycharmProjects\dataHandle\log\{0}'.format(out.id + '.json'), 'w').write(
        json.dumps(out.toJson()))
    return time_s
