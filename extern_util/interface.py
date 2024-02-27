import json
import os
import shutil
import time

from database.mysql.experiment.experiment_dao import ExperimentDao
from database.mysql.experiment.experiment_data import ExperimentOne, ExperimentCome
from extern_util.train_data_gen import train_for_kgan, train_for_aen_atae
from extern_util.absa_arg import KGANModelArg, ABSAModelArg
from database.mysql.dataset.daset_data import Sentence, Scene


class ABSAModelRunner:
    @classmethod
    def for_kgan_laptop(cls, aug_sentences: [Sentence]):
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
            seeds=[14, 131, 137, 257, 511, 1023]
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
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_kgan_rest(cls, aug_sentences: [Sentence]):
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
            seeds=[14, 131, 137, 257, 511, 1023]
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
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
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
            seeds=[131, 137, 257, 511, 1013, 2047, 4095, 8097],
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
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_atae_rest(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.atae_lstm_command,
            dataset='restaurant',
            lr=0.0012,
            dropout=0.55,
            num_epoch=20,
            batch_size=64,
            patience=5,
            seeds=[31, 37, 157, 411, 913, 2037, 4085, 8087],
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
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_atae_twitter(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.atae_lstm_command,
            dataset='twitter',
            lr=0.0012,
            dropout=0.55,
            num_epoch=20,
            batch_size=64,
            patience=5,
            seeds=[31, 37, 157, 411, 913, 2037, 4085, 8087],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='atae',
            dataset='twitter',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_mem_laptop(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.mem_command,
            dataset='laptop',
            lr=0.0011,
            dropout=0.1,
            num_epoch=30,
            batch_size=32,
            patience=8,
            seeds=[131, 137, 257, 511, 1013, 2047, 4095, 8097],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='mem',
            dataset='laptop',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_mem_rest(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.mem_command,
            dataset='restaurant',
            lr=0.0011,
            dropout=0.1,
            num_epoch=30,
            batch_size=48,
            patience=8,
            seeds=[131, 137, 257, 511, 1013, 2047, 4095, 8097],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='mem',
            dataset='restaurant',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))

    @classmethod
    def for_mem_twitter(cls, aug_sentences: [Sentence]):
        train_for_aen_atae(aug_sentences, './tmp/tmp.txt')
        arg = ABSAModelArg(
            command=ABSAModelArg.mem_command,
            dataset='twitter',
            lr=0.0011,
            dropout=0.1,
            num_epoch=30,
            batch_size=64,
            patience=8,
            seeds=[131, 137, 257, 511, 1013, 2047, 4095, 8097],
            valset_ratio=0.2,
            train_file=r'C:\Users\16230\PycharmProjects\dataHandle\tmp\tmp.txt'
        )
        jsons = arg.run()
        return saveExperiment(ExperimentCome(
            id=time.time().__str__(),
            absa_model='mem',
            dataset='twitter',
            learning_rate=arg.lr,
            dropout_rate=arg.dropout,
            n_epoch=arg.num_epoch,
            bs=arg.batch_size,
            patience=arg.patience,
            seeds=arg.seeds,
            valset_ratio=arg.valset_ratio,
            outcomes=ExperimentOne.fromOutcomes(jsons),
            ids=ExperimentOne.getIds(aug_sentences),
            method='',
            chat_model='',
        ))


def saveExperiment(out: ExperimentCome):
    return out


for_someone_atae = {
    Scene.restaurant.name: [
        # ABSAModelRunner.for_mem_rest,
        ABSAModelRunner.for_atae_rest,
        # ABSAModelRunner.for_kgan_rest, #效果不好
    ],
    Scene.laptop.value: [
        # ABSAModelRunner.for_mem_laptop,
        ABSAModelRunner.for_atae_laptop,
        # ABSAModelRunner.for_kgan_laptop, #效果不好
    ],
    # Scene.twitter.value: [
    #     # ABSAModelRunner.for_mem_twitter,
    #     ABSAModelRunner.for_atae_twitter,
    #     # ABSAModelRunner.for_kgan_laptop, #效果不好
    # ]
}

for_someone_mem = {
    Scene.restaurant.name: [
        ABSAModelRunner.for_mem_rest,
        # ABSAModelRunner.for_atae_rest,
        # ABSAModelRunner.for_kgan_rest, #效果不好
    ],
    Scene.laptop.value: [
        ABSAModelRunner.for_mem_laptop,
        # ABSAModelRunner.for_atae_laptop,
        # ABSAModelRunner.for_kgan_laptop, #效果不好
    ],
    # Scene.twitter.value: [
    #     ABSAModelRunner.for_mem_twitter,
    #     # ABSAModelRunner.for_atae_twitter,
    #     # ABSAModelRunner.for_kgan_laptop, #效果不好
    # ]
}


def start_experiment_atae(scene: str, sentences: list[Sentence], chat_model: str, method: str):
    dao = ExperimentDao()
    # get_experiments()
    for function in for_someone_atae[scene]:
        if exist_experiment(chat_model, method):
            continue
        come = function(aug_sentences=sentences)
        if come.method == "":
            come.chat_model = chat_model
        come.method = method
        open(r'C:\Users\16230\PycharmProjects\dataHandle\log\{0}'.format(come.id + '.json'), 'w').write(
            json.dumps(come.toJson()))
        dao.put(come)


def start_experiment_mem(scene: str, sentences: list[Sentence], chat_model: str, method: str):
    dao = ExperimentDao()
    # get_experiments()
    for function in for_someone_mem[scene]:
        if exist_experiment(chat_model, method):
            continue
        come = function(aug_sentences=sentences)
        if come.method == "":
            come.chat_model = chat_model
        come.method = method
        open(r'C:\Users\16230\PycharmProjects\dataHandle\log\{0}'.format(come.id + '.json'), 'w').write(
            json.dumps(come.toJson()))
        dao.put(come)


experiments = []


def exist_experiment(chat_model: str, method: str):
    for experiment in experiments:
        if (experiment.chat_model == chat_model) & (experiment.method == method):
            experiments.remove(experiment)
            print('recover from {0} {1}'.format(chat_model, method))
            return True
    return False


def get_experiments():
    if len(experiments) != 0:
        return
    for file in os.listdir(r'C:\Users\16230\PycharmProjects\dataHandle\log'):
        if os.path.isfile(r'C:\Users\16230\PycharmProjects\dataHandle\log\\' + file):
            t = float(file.replace('.json', ''))
            f = r'C:\Users\16230\PycharmProjects\dataHandle\log\\' + file
            come = ExperimentCome.fromJson(open(f).read(), tid=t)
            experiments.append(come)
