from database.mysql.experiment.experiment_data import ExperimentCome
from database.mysql.experiment.experiment_table import Experiment


class ExperimentDao:
    experiments = []

    def __init__(self):
        Experiment.create_dataset_table()
        self.datas = []

    def put(self, experiment: ExperimentCome):
        Experiment.save_experiment(experiment=experiment)

    def puts(self, experiments: [ExperimentCome]):
        for experiment in experiments:
            self.put(experiment)

    def getExperiments(self) -> list[ExperimentCome]:
        if len(ExperimentDao.experiments) != 0:
            return ExperimentDao.experiments
        ExperimentDao.experiments = Experiment.get_experiments()
        return self.getExperiments()

    def getSpecExperiments(self, absa_model, chat_model, method_pattern, dataset) -> list[ExperimentCome]:
        specs = []
        for e in self.getExperiments():

            ifAdd = True
            ifAdd &= e.absa_model == absa_model
            if e.method != method_pattern:
                ifAdd &= e.chat_model == chat_model
            ifAdd &= e.method.__contains__(method_pattern)
            ifAdd &= e.dataset == dataset
            if ifAdd:
                specs.append(e)
        return specs

    def experimentExist(self, model: str, method: str, scene: str):
        return Experiment.experiment_exist(method=method, chat_model=model, scene=scene)

    # def experimentDelete(self):
    #     return Experiment.
