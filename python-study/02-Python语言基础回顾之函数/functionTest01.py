# 关键字参数
# 函数调用，通过“键=值”形式加以指定。
# 可以让函数更加清晰、容易使用，同时也清除了参数的顺序需求。
def user_info(name, age, gender):
    print(f'您的名字是{name}, 年龄是{age}, 性别是{gender}')
user_info('Rose', age=20, gender='女')
user_info('小明', gender='男', age=16)

# 缺省参数
'''
缺省参数也叫默认参数，用于定义函数，为参数提供默认值，调用
函数时可不传该默认参数的值（注意：所有位置参数必须出现在默
认参数前，包括函数定义和调用）。
'''
def user_info(name, age, gender='男'):
    print(f'您的名字是{name}, 年龄是{age}, 性别是{gender}')
user_info('TOM', 20)
user_info('Rose', 18, '女')

# 不定长参数
'''
不定长参数也叫可变参数。用于不确定调用的时候会传递多少个参
数(不传参也可以)的场景。此时，可用包裹(packing)位置参数，或
者包裹关键字参数，来进行参数传递，会显得非常方便。
'''
def user_info(*args):
    print(args)
# ('TOM',)
user_info('TOM')
# ('TOM', 18)
user_info('TOM', 18)

# 注意：传进的所有参数都会被args变量收集，它会根据传进参数的位置合并为一个元组(tuple)，
# args是元组类型，这就是包裹位置传递。
# 包裹关键字传递
def user_info(**kwargs):
    print(kwargs)
# {'name': 'TOM', 'age': 18, 'id': 110}
user_info(name='TOM', age=18, id=110)

# 拆包：元组
def return_num():
    return 100, 200
num1, num2 = return_num()
print(num1)  # 100
print(num2)  # 200

# 拆包：字典
dict1 = {'name': 'TOM', 'age': 18}
a, b = dict1
# 对字典进行拆包，取出来的是字典的key
print(a)  # name
print(b)  # age
print(dict1[a])  # TOM
print(dict1[b])  # 18

# 交换变量值
a, b = 1, 2
a, b = b, a
print(a)  # 2
print(b)  # 1

'''
在python中，值是靠引用来传递来的。
我们可以用id() 来判断两个变量是否为同一个值的引用。 
我们可以将id值理解为那块内存的地址标识。
'''
# 1. int类型
a = 1
b = a
print(b)  # 1
print(id(a))  # 140708464157520
print(id(b))  # 140708464157520

a = 2
print(b)  # 1,说明int类型为不可变类型
print(id(a))  # 140708464157552，此时得到是的数据2的内存地址
print(id(b))  # 140708464157520 ,b不变

# 2. 列表 改变元素的值，地址值不变
aa = [10, 20]
bb = aa
print(id(aa))  # 2325297783432
print(id(bb))  # 2325297783432
aa.append(30)
print(bb)  # [10, 20, 30], 列表为可变类型
print(id(aa))  # 2325297783432
print(id(bb))  # 2325297783432

print('-'*10)

# 引用当做实参
def test1(a):
    print(a)
    print(id(a))
    a += a
    print(a)
    print(id(a))
# int：计算前后id值不同
b = 100
test1(b)
# 列表：计算前后id值相同
c = [11, 22]
test1(c)

# 所谓可变类型与不可变类型是指：数据能够直接进行修改，
# 如果能直接修改那么就是可变，否则是不可变.
'''
可变类型:
1.列表
2.字典
3.集合

不可变类型:
1.整型
2.浮点型
3.字符串
4.元组
'''


# lambda语法:如果一个函数有一个返回值，并且只有一句代码，可以使用 lambda 简化。
# lambda 参数列表:表达式
'''
注意:
1.lambda表达式的参数可有可无，函数的参数在lambda表达式中完全适用。
2.lambda表达式能接收任何数量的参数但只能返回一个表达式的值。
'''
# 函数
def fn1():
    return 200
print(fn1)
print(fn1())
# lambda表达式
fn2 = lambda: 100
print(fn2)
print(fn2())
