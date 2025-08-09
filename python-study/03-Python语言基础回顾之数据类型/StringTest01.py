# 一、认识字符串
a = 'hello world'
b = "abcdefg"
print(type(a))
print(type(b))

name3 = ''' Tom '''
name4 = """ Rose """
# 三引号形式的字符串支持换行。
a = ''' i am Tom,
       nice to meet you! '''
b = """ i am Rose,
       nice to meet you! """
# 创建一个字符串 I'm Tom
c = "I'm Tom"
d = 'I\'m Tom'

print('hello world')

name = 'Tom'
print('我的名字是%s' % name)
print(f'我的名字是{name}')

name = input('请输入您的名字：')
print(f'您输入的名字是{name}')
print(type(name))
password = input('请输入您的密码：')
print(f'您输入的密码是{password}')
print(type(password))

name = "abcdef"
print(name[1])
print(name[0])
print(name[2])

# 切片 : 序列[开始位置下标:结束位置下标:步长]
'''
1. 不包含结束位置下标对应的数据， 正负整数均可。
2. 步长是选取间隔，正负整数均可，默认步长为1。
'''
name = "abcdefg"
print(name[2:5:1])  # cde
print(name[2:5])  # cde
print(name[:5])  # abcde
print(name[1:])  # bcdefg
print(name[:])  # abcdefg
print(name[::2])  # aceg
print(name[:-1])  # abcdef, 负1表示倒数第一个数据
print(name[-4:-1])  # def
print(name[::-1])  # gfedcba

# 查找 : 字符串序列.find(子串, 开始位置下标, 结束位置下标)
# find() : 检测某个子串是否包含在这个字符串中，如果在返回这个子串开始的位置下标，否则则返回-1。
# 注意 : 开始和结束位置下标可以省略，表示在整个字符串序列中查找。
mystr = 'hello world and itcast and itheima and Python'
#        0123456789
print(mystr.find('and'))  # 12
print(mystr.find('and', 15, 30))  # 23
print(mystr.find('ands'))  # -1

# index()：检测某个子串是否包含在这个字符串中，如果在返回这个子串开始的位置下标，否则则报异常。
# 字符串序列.index(子串, 开始位置下标, 结束位置下标)
mystr = "hello world and itcast and itheima and Python"
print(mystr.index('and'))  # 12
print(mystr.index('and', 15, 30))  # 23
# print(mystr.index('ands'))  # 报错

# rfind()： 和find()功能相同，但查找方向为右侧开始。
# rindex()：和index()功能相同，但查找方向为右侧开始。

# count()：返回某个子串在字符串中出现的次数
# 字符串序列.count(子串, 开始位置下标, 结束位置下标)
# 注意：开始和结束位置下标可以省略，表示在整个字符串序列中查找。
mystr = "hello world and itcast and itheima and Python"
print(mystr.count('and'))  # 3
print(mystr.count('ands'))  # 0
print(mystr.count('and', 0, 20))  # 1

# 修改 : 所谓修改字符串，指的就是通过函数的形式修改字符串中的数据。
# replace()：替换
# 字符串序列.replace(旧子串, 新子串, 替换次数)
'''
注意：数据按照是否能直接修改分为可变类型和不可变类型两
种。字符串类型的数据修改的时候不能改变原有字符串，属于
不能直接修改数据的类型即是不可变类型。
'''
mystr = "hello world and itcast and itheima and Python"
# 结果：hello world he itcast he itheima he Python
print(mystr.replace('and', 'he'))
# 结果：hello world he itcast he itheima he Python
print(mystr.replace('and', 'he', 10))
# 结果：hello world and itcast and itheima and Python
print(mystr)

# split()：按照指定字符分割字符串。
# 字符串序列.split(分割字符, num)
# 注意：num表示的是分割字符出现的次数，即将来返回数据个数为num+1个。
# 注意：如果分割字符是原有字符串中的子串，分割后则丢失该子串。
mystr = "hello world and itcast and itheima and Python"
# 结果：['hello world ', ' itcast ', ' itheima ',' Python']
print(mystr.split('and'))
# 结果：['hello world ', ' itcast ', ' itheima and Python']
print(mystr.split('and', 2))
# 结果：['hello', 'world', 'and', 'itcast', 'and', 'itheima', 'and', 'Python']
print(mystr.split(' '))
# 结果：['hello', 'world', 'and itcast and itheima and Python']
print(mystr.split(' ', 2))

# join()：用一个字符或子串合并字符串，即是将多个字符串合并为一个新的字符串。
# 字符或子串.join(多字符串组成的序列)
list1 = ['chuan', 'zhi', 'bo', 'ke']
t1 = ('aa', 'b', 'cc', 'ddd')
# 结果：chuan_zhi_bo_ke
print('_'.join(list1))
# 结果：aa...b...cc...ddd
print('...'.join(t1))

# capitalize()：将字符串第一个字符转换成大写。
mystr = "hello world and itcast and itheima and Python"
# 结果：Hello world and itcast and itheima and python
print(mystr.capitalize())

# title()：将字符串每个单词首字母转换成大写。
mystr = "hello world and itcast and itheima and Python"
# 结果：Hello World And Itcast And Itheima And Python
print(mystr.title())

# lower()：将字符串中大写转小写。
# upper()：将字符串中小写转大写。
# strip()：删除字符串左侧空白字符。
# rstrip()：删除字符串右侧空白字符。
# strip()：删除字符串两侧空白字符。

# ljust()：返回一个原字符串左对齐,并使用指定字符(默认空格)填充至对应长度 的新字符串。
mystr = 'hello'
print(mystr.ljust(10, '.')) # hello.....

# rjust()：返回一个原字符串右对齐,并使用指定字符(默认空格)填充至对应长度 的新字符串，语法和ljust()相同。
print(mystr.rjust(10, '.')) # .....hello

# center()：返回一个原字符串居中对齐,并使用指定字符(默认空格)填充至对应长度 的新字符串，语法和ljust()相同。
print(mystr.center(10, '.')) # ..hello...

# 判断
# startswith()：检查字符串是否是以指定子串开头，是则返回True，否则返回 False。如果设置开始和结束位置下标，则在指定范围内检查。
# 字符串序列.startswith(子串, 开始位置下标, 结束位置下标)
mystr = "hello world and itcast and itheima and Python   "
# 结果：True
print(mystr.startswith('hello'))
# 结果False
print(mystr.startswith('hello', 5, 20))

# endswith()：：检查字符串是否是以指定子串结尾，是则返回True，否则返回 False。如果设置开始和结束位置下标，则在指定范围内检查。
# 字符串序列.endswith(子串, 开始位置下标, 结束位置下标)
mystr = "hello world and itcast and itheima and Python"
# 结果：True
print(mystr.endswith('Python'))
# 结果：False
print(mystr.endswith('python'))
# 结果：False
print(mystr.endswith('Python', 2, 20))

# isalpha()：如果字符串至少有一个字符并且所有字符都是字母则返回 True, 否则返回 False。
mystr1 = 'hello'
mystr2 = 'hello12345'
# 结果：True
print(mystr1.isalpha())
# 结果：False
print(mystr2.isalpha())

# isdigit()：如果字符串只包含数字则返回 True 否则返回 False。
mystr1 = 'aaa12345'
mystr2 = '12345'
# 结果： False
print(mystr1.isdigit())
# 结果：True
print(mystr2.isdigit())

# isalnum()：如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True,否则返回 False。
mystr1 = 'aaa12345'
mystr2 = '12345-'
# 结果：True
print(mystr1.isalnum())
# 结果：False
print(mystr2.isalnum())

# isspace()：如果字符串中只包含空白，则返回 True，否则返回False。
mystr1 = '1 2 3 4 5'
mystr2 = '     '
# 结果：False
print(mystr1.isspace())
# 结果：True
print(mystr2.isspace())