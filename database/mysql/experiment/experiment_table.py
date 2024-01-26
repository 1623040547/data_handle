from database.mysql.db import Database
from database.mysql.experiment.experiment_data import ExperimentCome, ExperimentOne

_db = Database('experiment')


class TableName:
    experiment = "experiment"
    outcome = "outcome"


class Table:
    experiment = TableName.experiment + """(
    id varchar(64) primary key,
    absa_model varchar(128),
    dataset varchar(128),
    learning_rate float,
    dropout_rate float(9,8),
    n_epoch int(8),
    bs int(8),
    patience int(8),
    valset_ratio float(9,8),
    ids LONGBLOB,
    method varchar(512)
    )
"""
    outcome = TableName.outcome + """(
    id int(8) primary key auto_increment,
    seed int(8),
    test_acc float(31,30),
    test_f1 float(31,30),
    epoch int(8),
    experimentId varchar(64),
    foreign key(experimentId) references experiment(id)
    )
    """


class Experiment:
    @classmethod
    def create_dataset_table(cls):
        """
        创建用于存储ABSA数据集的关系表格，
        prompt代表生成此条数据所用模板，原始数据无模板，
        sentence为此条数据文本内容，
        aspect代表sentence中所拥有的方面信息，
        sentence_aspect代表aspect在sentence中的情感
        """
        _db.create_table(Table.experiment)
        _db.create_table(Table.outcome)

    @classmethod
    def save_experiment(cls, experiment: ExperimentCome):
        suc = True
        if cls.__save_experiment(experiment):
            for out in experiment.outcomes:
                suc &= cls.__save_outcome(out, experimentId=experiment.id)
        else:
            return False
        if suc:
            _db.save()
            return True

    @classmethod
    def __save_experiment(cls, experiment: ExperimentCome):
        print(experiment.ids)
        print(experiment.toIds())
        print(experiment.fromIds(experiment.toIds()))
        return _db.insert(
            TableName.experiment + '(`id`,`absa_model`,`dataset`,`learning_rate`,`dropout_rate`,`n_epoch`,`bs`,'
            + '`patience`,`valset_ratio`,`ids`,`method`)',
            '\'{0}\',\'{1}\',\'{2}\',{3},{4},{5},{6},{7},{8},\'{9}\',\'{10}\''.format(
                experiment.id,
                experiment.absa_model,
                experiment.dataset,
                experiment.learning_rate,
                experiment.dropout_rate,
                experiment.n_epoch,
                experiment.bs,
                experiment.patience,
                experiment.valset_ratio,
                experiment.toIds(),
                experiment.method,
            )
        ) > 0

    @classmethod
    def __save_outcome(cls, outcome: ExperimentOne, experimentId: str):
        print(outcome.test_acc)
        print(outcome.test_f1)
        print(outcome.epoch)
        print(outcome.seed)
        print(experimentId)
        return _db.insert(TableName.outcome + '(`seed`,`test_acc`,`test_f1`,`epoch`,`experimentId`)',
                          '{0},{1},{2},{3},\'{4}\''
                          .format(
                              outcome.seed,
                              outcome.test_acc,
                              outcome.test_f1,
                              outcome.epoch,
                              experimentId,
                          )
                          ) > 0

    @classmethod
    def __get_outcomes(cls, experimentId: str):
        outcomes = []
        datas = _db.select(table=TableName.outcome, sel='seed,test_acc,test_f1,epoch',
                           condition='experimentId = \'{0}\''.format(experimentId))
        for data in datas:
            outcome = ExperimentOne(
                seed=data[0],
                test_acc=data[1],
                test_f1=data[2],
                epoch=data[3],
            )
            outcomes.append(outcome)
        return outcomes

    @classmethod
    def get_experiments(cls):
        experiments = []
        datas = _db.select(table=TableName.experiment, sel='id,absa_model,dataset,learning_rate,dropout_rate,'
                                                           'n_epoch,bs,patience,valset_ratio,ids,method',
                           condition='id != \'\'')
        for data in datas:
            outcomes = cls.__get_outcomes(data[0])
            seeds = [a.seed for a in outcomes]
            experiment = ExperimentCome(
                id=data[0],
                absa_model=data[1],
                dataset=data[2],
                learning_rate=data[3],
                dropout_rate=data[4],
                n_epoch=data[5],
                bs=data[6],
                patience=data[7],
                valset_ratio=data[8],
                ids=ExperimentCome.fromIds(data[9]),
                seeds=seeds,
                outcomes=outcomes,
                method=data[10]
            )
            experiments.append(experiment)
            return experiment
