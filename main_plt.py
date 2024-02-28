import os
from enum import Enum
import seaborn as sns
import matplotlib.pyplot as plt
from database.mysql.experiment.experiment_data import ExperimentCome


class Method(Enum):
    ATAE_LSTM = "atae"
    MemNet = "mem"


class Dataset(Enum):
    laptop = "laptop"
    restaurant = "rest"
    twitter = "twitter"


class Experiment(Enum):
    aeda = "aeda"
    eda = "eda"
    complex_02 = "complex_0.2"
    complex_05 = "complex_0.5"
    complex_08 = "complex_0.8"
    chat_glm_turbo = "glm"
    chat_35_turbo = "gpt"
    llama_70_chat = "llama"


def draw_pic(method: Method, dataset: Dataset, experiments: [Experiment], desc: str):
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
            max_y = max(max_y, baseline.best_f1())
            min_y = min(min_y, baseline.best_f1())
            break
    for e in experiments:
        y = [baseline.best_f1()]
        p = path + '\\' + method.value + '\\' + dataset.value + '\\' + e.value
        chat_model = ""
        for f in os.listdir(p):
            t = float(f.replace('.json', ''))
            f = p + '\\' + f
            come = ExperimentCome.fromJson(open(f).read(), tid=t)
            chat_model = come.chat_model
            acc = come.best_f1()
            y.append(acc)
            max_y = max(max_y, acc)
            min_y = min(min_y, acc)
        yy[chat_model] = y
    ###图形绘制
    # 设置字体
    font = {'family': 'Times New Roman',
            'size': 12}
    plt.rc('font', **font)

    # 绘图
    sns.set_style("whitegrid")  # 设置背景样式

    count = 0
    for k, v in yy.items():
        sns.lineplot(x=x, y=v, color=colors[count], linewidth=2.0, marker="o", markersize=8, markeredgecolor="white",
                     markeredgewidth=1.5, label=k)
        count += 1

    title = "{0}({1})".format(dataset.value, method.value)
    # 添加标题和标签
    plt.title(title, fontweight='bold', fontsize=14)
    plt.xlabel("Ratio", fontsize=12)
    plt.ylabel("F1 Best", fontsize=12)

    # 添加图例
    plt.legend(loc='upper left', frameon=True, fontsize=10)

    # 设置刻度字体和范围
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlim(0, max_x)
    plt.ylim(min_y - 0.0005, max_y + 0.0005)

    # 设置坐标轴样式
    for spine in plt.gca().spines.values():
        spine.set_edgecolor("#CCCCCC")
        spine.set_linewidth(1.5)

    plt.savefig(r'C:\Users\16230\PycharmProjects\dataHandle\pic\{0}_{1}.png'.format(title, desc), dpi=300,
                bbox_inches='tight')
    plt.figure()
    # # 显示图像
    # plt.show()


normal = [
    Experiment.eda,
    Experiment.aeda,
    Experiment.chat_glm_turbo,
    Experiment.chat_35_turbo,
    Experiment.llama_70_chat,
]

complex = [
    Experiment.eda,
    Experiment.aeda,
    Experiment.complex_02,
    Experiment.complex_05,
    Experiment.complex_08,
]

draw_pic(Method.ATAE_LSTM, Dataset.laptop, experiments=normal, desc='normal')
draw_pic(Method.ATAE_LSTM, Dataset.laptop, experiments=complex, desc='complex')

draw_pic(Method.ATAE_LSTM, Dataset.restaurant, experiments=normal, desc='normal')
draw_pic(Method.ATAE_LSTM, Dataset.restaurant, experiments=complex, desc='complex')

draw_pic(Method.ATAE_LSTM, Dataset.twitter, experiments=normal, desc='normal')
draw_pic(Method.ATAE_LSTM, Dataset.twitter, experiments=complex, desc='complex')

draw_pic(Method.MemNet, Dataset.laptop, experiments=normal, desc='normal')
draw_pic(Method.MemNet, Dataset.laptop, experiments=complex, desc='complex')

draw_pic(Method.MemNet, Dataset.restaurant, experiments=normal, desc='normal')
draw_pic(Method.MemNet, Dataset.restaurant, experiments=complex, desc='complex')

draw_pic(Method.MemNet, Dataset.twitter, experiments=normal, desc='normal')
draw_pic(Method.MemNet, Dataset.twitter, experiments=complex, desc='complex')
