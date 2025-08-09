#TextProBarV2.py
import time
for i in range(101):
    #end="" 表示在末尾增加信息,空字符串则表示打印完光标停留在最后不换行
    print("\r{:3}%".format(i),end="")
    time.sleep(0.1)
