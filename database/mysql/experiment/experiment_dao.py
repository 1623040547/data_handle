from database.mysql.experiment.experiment_data import ExperimentCome
from database.mysql.experiment.experiment_table import Experiment


class ExperimentDao:
    def __init__(self):
        Experiment.create_dataset_table()
        self.datas = []

    def put(self, experiment: ExperimentCome):
        Experiment.save_experiment(experiment=experiment)

    def puts(self, experiments: [ExperimentCome]):
        for experiment in experiments:
            self.put(experiment)
