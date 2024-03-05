import os
from enum import Enum
import seaborn as sns
import matplotlib.pyplot as plt
from database.mysql.experiment.experiment_data import OutcomeMethod, ExperimentCome
import scipy.stats as st
import pandas as pd


class Method(Enum):
    ATAE_LSTM = "atae"
    MemNet = "mem"


def fixed_y_liner(x, y):
    y0 = y[0]
    sum_xy = 0
    sum_xx = 0
    for i in range(len(x)):
        sum_xx += x[i] * x[i]
        sum_xy += x[i] * (y[i] - y0)
    return sum_xy / sum_xx


class Dataset(Enum):
    laptop = "laptop"
    restaurant = "rest"
    twitter = "twitter"


class Experiment(Enum):
    aeda = "aeda"
    eda = "eda"
    complex = "complex"
    complex_02 = "complex_0.2"
    complex_05 = "complex_0.5"
    complex_08 = "complex_0.8"
    chat_glm_turbo = "glm"
    chat_35_turbo = "gpt"
    llama_70_chat = "llama"
    chat_glm_turbo_x = "glm_x"
    chat_35_turbo_x = "gpt_x"
    llama_70_chat_x = "llama_x"


def draw_pic(method: Method, dataset: Dataset, experiments: [Experiment], m: OutcomeMethod):
    ###变量定义
    path = r'C:\Users\16230\PycharmProjects\dataHandle\log'
    colors = [
        "#038355",
        "#ffc34e",
        "#4A90E2",
        "#8B572A",
        "#9013FE",
        "#B8E986",
        "#F5A623",
        "#264263",
    ]

    yy = {}
    max_y = 0
    min_y = 1
    baseline = None

    if dataset.value == Dataset.twitter.value:
        x = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        max_x = 2.25
    else:
        x = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
        max_x = 2.75

    ###数据加载
    p = path + '\\' + method.value + '\\' + dataset.value
    for f in os.listdir(p):
        if f.__contains__('.json'):
            t = float(f.replace('.json', ''))
            f = p + '\\' + f
            baseline = ExperimentCome.fromJson(open(f).read(), tid=t)
            max_y = max(max_y, baseline.my_method(m))
            min_y = min(min_y, baseline.my_method(m))
            break
    for e in experiments:
        y = [baseline.my_method(m)]
        p = path + '\\' + method.value + '\\' + dataset.value + '\\' + e.value
        chat_model = ""
        for f in os.listdir(p):
            t = float(f.replace('.json', ''))
            f = p + '\\' + f
            come = ExperimentCome.fromJson(open(f).read(), tid=t)
            chat_model = come.chat_model
            acc = come.my_method(m)
            y.append(acc)
        yy[chat_model] = y
    ###图形绘制
    # 设置字体
    font = {'family': 'Times New Roman',
            'size': 12}
    plt.rc('font', **font)

    # 绘图
    sns.set_style("whitegrid")  # 设置背景样式

    count = 0
    for k, y in yy.items():
        # 线性拟合，可以返回斜率，截距，r 值，p 值，标准误差
        slope = fixed_y_liner(x, y)
        new_y = []
        for x_value in x:
            v = slope * x_value + y[0]
            new_y.append(v)
            max_y = max(max_y, v)
            min_y = min(min_y, v)
        sns.lineplot(x=x, y=new_y, color=colors[count], linewidth=2.0, marker="o", markersize=6,
                     markeredgecolor="white",
                     markeredgewidth=1.5, label=k)
        count += 1

    title = "{0}({1})".format(dataset.value, method.value)
    # 添加标题和标签
    plt.title(title, fontweight='bold', fontsize=14)
    plt.xlabel("Ratio", fontsize=12)
    plt.ylabel(m.value, fontsize=12)

    # 添加图例
    plt.legend(loc='upper left', frameon=True, fontsize=10)

    # 设置刻度字体和范围
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlim(0, max_x)
    offset = (max_y - min_y) * 0.05
    plt.ylim(min_y - offset, max_y + offset)

    # 设置坐标轴样式
    for spine in plt.gca().spines.values():
        spine.set_edgecolor("#CCCCCC")
        spine.set_linewidth(1.5)

    plt.savefig(r'C:\Users\16230\PycharmProjects\dataHandle\pic\{0}_{1}.png'.format(m.value.replace(' ', '_'), title),
                dpi=300,
                bbox_inches='tight')
    plt.close()
    # # 显示图像
    # plt.show()


normal = [
    Experiment.eda,
    Experiment.aeda,
    Experiment.chat_glm_turbo,
    Experiment.chat_35_turbo,
    Experiment.llama_70_chat,
]

normal_x = [
    Experiment.eda,
    Experiment.aeda,
    Experiment.chat_glm_turbo_x,
    Experiment.chat_35_turbo_x,
    Experiment.llama_70_chat_x,
]

complex = [
    Experiment.chat_35_turbo,
    Experiment.complex,
    Experiment.complex_02,
    Experiment.complex_05,
    Experiment.complex_08,
]

compare_llama = [
    Experiment.llama_70_chat_x,
    Experiment.llama_70_chat,
]

compare_gpt = [
    Experiment.chat_35_turbo_x,
    Experiment.chat_35_turbo,
]

compare_glm = [
    Experiment.chat_glm_turbo,
    Experiment.chat_glm_turbo_x,
]


def draw_pics(method: Method, dataset: Dataset, experiment):
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.f1_var)
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.f1)
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.f1_best)
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.acc)
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.acc_var)
    draw_pic(method, dataset, experiments=experiment, m=OutcomeMethod.acc_best)


draw_pics(Method.MemNet, Dataset.restaurant, experiment=normal_x)
draw_pics(Method.ATAE_LSTM, Dataset.restaurant, experiment=normal_x)
draw_pics(Method.MemNet, Dataset.laptop, experiment=normal_x)
draw_pics(Method.ATAE_LSTM, Dataset.laptop, experiment=normal_x)
# draw_pics(Method.MemNet, Dataset.twitter, experiment=normal)
# draw_pics(Method.ATAE_LSTM, Dataset.twitter, experiment=normal)
