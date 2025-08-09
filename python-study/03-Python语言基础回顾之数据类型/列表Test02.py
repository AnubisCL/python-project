# 二、 列表
# 列表可以一次性存储多个数据，但是列表中的数据允许更改。

# index()：返回指定数据所在位置的下标 。
# count()：统计指定数据在当前列表中出现的次数。
# len()：访问列表长度，即列表中数据的个数。

# in：判断指定数据在某个列表序列，如果在返回True，否则返回False
# not in：判断指定数据不在某个列表序列，如果不在返回True，否则返回False

# 增加：
# append()：列表结尾追加数据。
# 单个数据
name_list = ['Tom', 'Lily', 'Rose']
name_list.append('xiaoming')
# 结果：['Tom', 'Lily', 'Rose', 'xiaoming']
print(name_list)

# 如果append()追加的数据是一个序列，则追加整个序列到列表
# 序列数据
name_list = ['Tom', 'Lily', 'Rose', ['xiaoming', 'xiaohong']]
# 结果：['Tom', 'Lily', 'Rose', ['xiaoming','xiaohong']]
print(name_list)

# extend()：列表结尾追加数据，如果数据是一个序列，则将这个序列的数据逐一添加到列表。
# 单个数据
name_list = ['Tom', 'Lily', 'Rose']
name_list.extend('xiaoming')
# 结果：['Tom', 'Lily', 'Rose', 'x', 'i', 'a','o', 'm', 'i', 'n', 'g']
print(name_list)
# 序列数据
name_list = ['Tom', 'Lily', 'Rose']
name_list.extend(['xiaoming', 'xiaohong'])
# 结果：['Tom', 'Lily', 'Rose', 'xiaoming', 'xiaohong']
print(name_list)

# insert()：指定位置新增数据。
name_list = ['Tom', 'Lily', 'Rose']
name_list.insert(1, 'xiaoming')
# 结果：['Tom', 'xiaoming', 'Lily', 'Rose']
print(name_list)

# 删除：
# del 目标
# pop()：删除指定下标的数据(默认为最后一个)，并返回该数据。
name_list = ['Tom', 'Lily', 'Rose']
del_name = name_list.pop(1)
# 结果：Lily
print(del_name)
# 结果：['Tom', 'Rose']
print(name_list)

# remove()：移除列表中某个数据的第一个匹配项。
# clear()：清空列表

# 修改
# 逆置：reverse()
num_list = [1, 5, 2, 3, 6, 8]
num_list.reverse()
# 结果：[8, 6, 3, 2, 5, 1]
print(num_list)

# 排序：sort()
# 列表序列.sort( key=None, reverse=False)
# 注意：reverse表示排序规则，reverse = True 降序，reverse = False 升序（默认）
num_list = [1, 5, 2, 3, 6, 8]
num_list.sort()
# 结果：[1, 2, 3, 5, 6, 8]
print(num_list)

# 复制函数：copy()
name_list = ['Tom', 'Lily', 'Rose']
name_li2 = name_list.copy()
# 结果：['Tom', 'Lily', 'Rose']
print(name_li2)



