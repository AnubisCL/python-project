"""
导入模块的方式:
1.import 模块名
2.from 模块名 import 功能名
3.from 模块名 import *
4.import 模块名 as 别名
5.from 模块名 import 功能名 as 别名
"""
from my_module1 import my_test
from my_module2 import my_test
import dlib

my_test(1, 1)

"""
如果使用from .. import ..或from .. import *导入多个模
块的时候，且模块内有同名功能。当调用这个同名功能的时候，调
用到的是后面导入的模块的功能。
"""

""""
如果一个模块文件中有__all__变量，
当使用from xxx import *导入时，
只能导入这个列表中的元素。
"""
from my_module3 import *
testA()
# testB()  # __all__变量中只有 testA

# 导入包
# 方法一：
import mypackage.my_module1

mypackage.my_module1.info_print1()

# 方法二：
from mypackage import *
mypackage.my_module2.info_print2()