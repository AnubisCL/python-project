import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

# 准备时长数据
x = [1, 2, 3, 4]
name = ['class1', 'class2', 'class3', 'class4']

# 展现不同电影的时长分布状态
plt.figure(figsize=(10, 10), dpi=100)

# 画出饼图
plt.pie(x, labels=name, autopct='%.2f%%', explode=(0.1, 0.1, 0, 0),
        wedgeprops={'edgecolor': 'r',  # 内外框颜色
                    'linestyle': '--',  # 线型
                    'alpha': 0.5,  # 透明度
                    # 更多参考matplotlib.patches.Wedge

                    },
        textprops={'color': 'r',  # 文本颜色
                   'fontsize': 16,  # 文本大小
                   'fontfamily': 'Microsoft JhengHei',  # 设置微软雅黑字体
                   # 更多参考matplotlib.pyplot.text

                   })

plt.show()