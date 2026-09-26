# -*- coding: utf-8 -*-
"""机器学习三个最小项目。仅依赖 Python 标准库。
合成数据用于学习机制，不代表现实业务效果。先读注释，再逐段运行。
"""
import random
import math
from statistics import mean
from pathlib import Path
import csv

# 项目一：回归。自编房屋面积与价格，独立同分布合成样本。
rng = random.Random(7)
rows = [(rng.uniform(30,150), rng.gauss(0,12)) for _ in range(120)]
rows = [(x, 20 + 1.5*x + noise) for x, noise in rows]
rng.shuffle(rows)
train, test = rows[:90], rows[90:]
xmean = mean(x for x,y in train)
ymean = mean(y for x,y in train)
slope = sum((x-xmean)*(y-ymean) for x,y in train) / sum((x-xmean)**2 for x,y in train)
intercept = ymean - slope*xmean
mse = lambda pairs: mean((real-pred)**2 for real,pred in pairs)
baseline = mse([(y,ymean) for x,y in test])
linear = mse([(y,intercept+slope*x) for x,y in test])
print('项目一：合成回归')
print('样本数：训练',len(train),'测试',len(test))
print('截距、斜率：',round(intercept,4),round(slope,4))
print('均值基线测试MSE：',round(baseline,4),'直线测试MSE：',round(linear,4))
print('要回答：如果真实关系是弯曲的，直线还会好吗？这一次切分能代表所有数据吗？')
# 文件只写到脚本所在目录，不依赖你的当前工作目录。
with Path(__file__).with_name('合成回归数据.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['area','target']); w.writerows(rows)
assert len(train)==90 and len(test)==30

# 项目二：阈值与代价。固定的教学概率/标签，不声称训练过概率模型。
prob=[.05,.12,.2,.32,.42,.55,.65,.75,.85,.95]
truth=[0,0,1,0,1,0,1,1,0,1]
print('\n项目二：分类决策')
for threshold in [.2,.5,.8]:
    pred=[p>=threshold for p in prob]
    tp=sum(a and y==1 for a,y in zip(pred,truth))
    fp=sum(a and y==0 for a,y in zip(pred,truth))
    fn=sum(not a and y==1 for a,y in zip(pred,truth))
    precision=tp/(tp+fp) if tp+fp else float('nan')
    recall=tp/(tp+fn)
    print('阈值',threshold,'TP/FP/FN',tp,fp,fn,'Precision',round(precision,3),'Recall',round(recall,3),'代价(FN×5+FP)',fn*5+fp)
print('要回答：漏报昂贵时你选择哪个阈值？若将这些点当最终测试集，能否反复调参？')

# 项目三：一维 k-means。距离并列时选择第一个中心。
points=[0.,2.,3.,8.,9.,10.]
centers=[0.,10.]
print('\n项目三：聚类迭代')
for iteration in range(10):
    groups=[[],[]]
    for x in points:
        j=min(range(2),key=lambda j:abs(x-centers[j]))
        groups[j].append(x)
    # 空簇时这里保留旧中心；真实任务需要明确重新初始化等策略。
    updated=[mean(g) if g else centers[j] for j,g in enumerate(groups)]
    print('第',iteration+1,'轮，分组',groups,'更新中心',updated)
    if all(abs(a-b)<1e-10 for a,b in zip(centers,updated)):
        break
    centers=updated
loss=sum(min((x-c)**2 for c in centers) for x in points)
print('组内平方距离总和：',round(loss,4))
assert all(math.isfinite(c) for c in centers)
print('要回答：不同初始中心是否总给相同结果？两个簇是否证明现实中有两个真实类别？')
