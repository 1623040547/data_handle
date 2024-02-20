import json
import os
import shutil

from dataclasses import dataclass


@dataclass()
class ABSAModelArg:
    command: str
    dataset: str  # laptop restaurant
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

    mem_command = (r'C:\Users\16230\Desktop\ABSA-PyTorch-master\venv\Scripts\python.exe '
                        r'C:\Users\16230\Desktop\ABSA-PyTorch-master\extern_util\mem_inter.py')

    def run(self):
        cmd = self.command + (
            ' --dataset={0} --lr={1} --dropout={2} --num_epoch={3} --batch_size={4} --patience={5} '
            '--seeds {6} --valset_ratio={7} --train_file={8}'
            .format(self.dataset, self.lr, self.dropout, self.num_epoch,
                    self.batch_size, self.patience, ' '.join([str(x) for x in self.seeds]),
                    self.valset_ratio, self.train_file))
        result = os.system(cmd)
        print(result)
        f = open(self.train_file + '.outcome.json', 'r').read()
        return f


@dataclass()
class KGANModelArg:
    ds_name: str
    dataset_name: str
    bs: int
    dropout_rate: float
    learning_rate: float
    n_epoch: int
    train_file: str
    seeds: list
    kgan_command = (r'C:\Users\16230\Desktop\KGAN-main\venv\Scripts\python.exe '
                    r'C:\Users\16230\Desktop\KGAN-main\main_total.py ')
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
        if os.path.exists(real_train_file):
            os.remove(real_train_file)
        shutil.copy(self.train_file, real_train_file)
        os.remove(self.train_file)
        cmd = self.kgan_command + (
            '--ds_name={0} --dataset_name={1} --bs={2} --dropout_rate={3} --learning_rate={4} --n_epoch={5} --seeds {6}'
            .format(self.ds_name, self.dataset_name, self.bs, self.dropout_rate,
                    self.learning_rate, self.n_epoch, ' '.join([str(x) for x in self.seeds])))
        os.system(cmd)
        f = open(real_train_file + '.outcome.json', 'r').read()
        return f
