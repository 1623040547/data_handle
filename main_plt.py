import os

import seaborn as sns
import matplotlib.pyplot as plt

from database.mysql.experiment.experiment_dao import ExperimentDao
from database.mysql.experiment.experiment_data import ExperimentCome

path = r'C:\Users\16230\PycharmProjects\dataHandle\log\log_atae_aeda_rest'
path2 = r'C:\Users\16230\PycharmProjects\dataHandle\log\log_atae_rest'
path3 = r'C:\Users\16230\PycharmProjects\dataHandle\log\log_atae_eda_rest'

x = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
x2 = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2,]

colors = [
    "#038355",  # 孔雀绿
    "#ffc34e",  # 向日黄
    "#0000ff",  # ?????
    "#00ffff",  # ?????
    "#ff0000",  # ?????
]

yy = {}
y0 = 0
y = []
# acc
for file in os.listdir(path):
    try:
        t = float(file.replace('.json', ''))
        f = path + '\\' + file
        come = ExperimentCome.fromJson(open(f).read(), tid=t)
        if come.method == "random_select_1_":
            y0 = come.acc()
        if len(y) == 0:
            y.append(y0)
        if come.method != "random_select_1_":
            y.append(come.acc())
        if len(y) == len(x):
            yy[come.chat_model] = y
            y = []
    except:
        continue

for file in os.listdir(path2):
    try:
        t = float(file.replace('.json', ''))
        f = path2 + '\\' + file
        come = ExperimentCome.fromJson(open(f).read(), tid=t)
        if come.method == "random_select_1_":
            y0 = come.acc()
        if len(y) == 0:
            y.append(y0)
        if come.method != "random_select_1_":
            y.append(come.acc())
        if len(y) == len(x2):
            y.append(0)
            y.append(0)
            yy[come.chat_model] = y
            y = []
    except:
        continue

for file in os.listdir(path3):
    try:
        t = float(file.replace('.json', ''))
        f = path3 + '\\' + file
        come = ExperimentCome.fromJson(open(f).read(), tid=t)
        if come.method == "random_select_1_":
            y0 = come.acc()
        if len(y) == 0:
            y.append(y0)
        if come.method != "random_select_1_":
            y.append(come.acc())
        if len(y) == len(x):
            yy[come.chat_model] = y
            y = []
    except:
        continue

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

# 添加标题和标签
plt.title("rest(atae)", fontweight='bold', fontsize=14)
plt.xlabel("Ratio", fontsize=12)
plt.ylabel("Avg Acc", fontsize=12)

# 添加图例
plt.legend(loc='upper left', frameon=True, fontsize=10)

# 设置刻度字体和范围
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(0, 3)
# plt.ylim(0.652, 0.700)
plt.ylim(0.74, 0.78)

# 设置坐标轴样式
for spine in plt.gca().spines.values():
    spine.set_edgecolor("#CCCCCC")
    spine.set_linewidth(1.5)

plt.savefig('./lineplot.png', dpi=300, bbox_inches='tight')
# 显示图像
plt.show()
