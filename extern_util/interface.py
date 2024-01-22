import json
import os
import shutil

from dataclasses import dataclass


@dataclass()
class ABSAModelArg:
    command: str
    dataset: str
    lr: float
    dropout: float
    num_epoch: int
    batch_size: int
    patience: int
    seeds: list
    valset_ratio: float
    train_file: str

    atae_lstm_command = ('C:\\Users\\16230\\Desktop\\ABSA-PyTorch-master\\venv\\Scripts\\python.exe '
                         'C:\\Users\\16230\\Desktop\\ABSA-PyTorch-master\\extern_util\\atae_lstm_inter.py')

    aen_bert_command = (r'C:\Users\16230\Desktop\ABSA-PyTorch-master\venv\Scripts\python.exe '
                        r'C:\Users\16230\Desktop\ABSA-PyTorch-master\extern_util\aen_bert_inter.py')

    def run(self):
        cmd = self.command + (
            ' --dataset={0} --lr={1} --dropout={2} --num_epoch={3} --batch_size={4} --patience={5} '
            '--seed {6} --valset_ratio={7} --train_file={8}'
            .format(self.dataset, self.lr, self.dropout, self.num_epoch,
                    self.batch_size, self.patience, ' '.join([str(x) for x in self.seeds]),
                    self.valset_ratio, self.train_file))
        result = os.system(cmd)
        print(result)
        f = open(self.train_file + '.outcome.json', 'r').read()
        f = json.loads(f)
        return f


@dataclass()
class KGANModelArg:
    ds_name: str
    dataset_name: str
    bs = 32
    dropout_rate = 0.5
    learning_rate = 0.001
    n_epoch = 20
    train_file: str
    kgan_command = r'C:\Users\16230\Desktop\KGAN-main\venv\Scripts\python.exe C:\Users\16230\Desktop\KGAN-main\main_total.py '
    ds_name_laptop = '14semeval_laptop'
    dataset_name_laptop = 'Laptop14'
    ds_name_rest = '14semeval_rest'
    dataset_name_rest = 'Rest14'

    def run(self):
        real_train_file = ''
        if self.ds_name == self.ds_name_laptop:
            real_train_file = r'C:\Users\16230\Desktop\KGAN-main\dataset\14semeval_laptop\train.txt'
        if self.ds_name == self.ds_name_rest:
            real_train_file = r'C:\Users\16230\Desktop\KGAN-main\dataset\14semeval_rest\train.txt'
        shutil.copy(self.train_file, real_train_file)
        cmd = self.kgan_command + (
            ' --ds_name={0} --dataset_name={1} --bs={2} --dropout_rate={3} --learning_rate={4} --n_epoch={5} '
            .format(self.ds_name, self.dataset_name, self.bs, self.dropout_rate,
                    self.learning_rate, self.n_epoch))
        result = os.system(cmd)
        print(cmd)
        f = open(real_train_file + '.outcome.json', 'r').read()
        f = json.loads(f)
        return f
