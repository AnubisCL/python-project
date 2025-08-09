# 认识数据类型
# 检测数据类型的方法：type()

a = 1
print(type(a))

b = 1.1
print(type(b))

c = True
print(type(c))

d = '12345'
print(type(d))

e = [10, 20, 30]
print(type(e))  # 序列

f = (10, 20, 30)
print(type(f))  # 元组

h = {10, 20, 30}
print(type(h))  # 集合

g = {'name': 'TOM', 'age': 20}
print(type(g))  # 字典

# 格式化输出
'''
%s 字符串
%d 有符号的十进制整数
%f 浮点数
'''

age = 18
name = 'TOM'
weight = 75.5
student_id = 1

print('我的名字是%s' % name)

print('我的学号是%4d' % student_id)

print('我的体重是%.2f公斤' % weight)

print('我的名字是%s，今年%d岁了' % (name, age))

print('我的名字是%s，明年%d岁了' % (name, age + 1))

print(f'我的名字是{name}, 明年{age + 1}岁了')

# 输入
password = input('请输入您的密码：')
print(f'您输入的密码是{password}')
print(type(password))

# 转换数据类型的作用
'''
int(x [,base ]) 将x转换为一个整数
float(x ) 将x转换为一个浮点数
str(x ) 将对象 x 转换为字符串
eval(str ) 用来计算在字符串中的有效Python表达式,并返回一个对象
tuple(s ) 将序列 s 转换为一个元组
list(s ) 将序列 s 转换为一个列表
'''

num = input('请输入您的幸运数字')
print(f" 您的幸运数字是{num}")
print(type(num))
print(type(int(num)))

# 实验
# 1. float() -- 转换成浮点型
num1 = 1
print(float(num1))
print(type(float(num1)))

# 2. str() -- 转换成字符串类型
num2 = 10
print(type(str(num2)))

# 3. tuple() -- 将一个序列转换成元组
lits1 = [10,20,30]
print(type(lits1))

# 4. list() -- 将一个序列转换成列表
t1 =  (100,200,300)
print(list(t1))
print(type(list(t1)))

# 5. eval() -- 将字符串中的数据转换成Python表达式原本类型
# 去掉最外层的双引号
str = "print('Hello')"
print(eval(str))    # Hello

# 逻辑运算符
'''
and | x and y
布尔"与"：如果 x 为 False，x
and y 返回 False，否则它返
回 y 的值。

or | x or y
布尔"或"：如果 x 是 True，
它返回 True，否则它返回 y
的值。

not | not x
布尔"非"：如果 x 为 True，
返回 False 。如果 x 为
False，它返回 True。
'''
a = 0
b = 1
c = 2
# and运算符，只要有一个值为0，则结果为0，否则结果为最后一个非0数字
print(a and b)  # 0
print(b and a)  # 0
print(a and c)  # 0
print(c and a)  # 0
print(b and c)  # 2
print(c and b)  # 1
# or运算符，只有所有值为0结果才为0，否则结果为第一个非0数字
print(a or b)  # 1
print(a or c)  # 2
print(b or c)  # 1

# 三目运算符
# 值1 if 条件 else 值2
a = 1
b = 2
c = a if a > b else b
print(c)
