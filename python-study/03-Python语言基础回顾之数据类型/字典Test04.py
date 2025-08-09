# 四、字典
'''
字典里面的数据是以键值对形式出现，字典数据和数据
顺序没有关系，即字典不支持下标，后期无论数据如何变化，只需
要按照对应的键的名字查找数据即可。

字典特点：
    1.符号为大括号
    2.数据为键值对形式出现
    3.各个键值对之间用逗号隔开
'''
# 有数据字典
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
# 空字典
dict2 = {}

# 增 写法：字典序列[key] = 值
# 注意：如果key存在则修改这个key对应的值；如果key不存在，则新增此键值对。
dict1['name'] = 'Rose'
# 结果：{'name': 'Rose', 'age': 20, 'gender':'男'}
print(dict1)
dict1['id'] = 110
# {'name': 'Rose', 'age': 20, 'gender': '男','id': 110}
print(dict1)

# 删 del() / del：删除字典或删除字典中指定键值对。
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
del dict1['gender']
# 结果：{'name': 'Tom', 'age': 20}
print(dict1)

# clear()：清空字典
dict1.clear()
print(dict1)  # {}

# 改 写法：字典序列[key] = 值
# 注意：如果key存在则修改这个key对应的值 ；如果key不存在则新增此键值对。

# key值查找
# 如果当前查找的key存在，则返回对应的值；否则则报错。
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
print(dict1['name'])  # Tom
# print(dict1['id'])  # 报错

# 字典序列.get(key, 默认值)
# 注意：如果当前查找的key不存在则返回第二个参数(默认值)，如果省略第二个参数，则返回None。

# keys() 获取所有的 key 值
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
print(dict1.keys())  # dict_keys(['name', 'age', 'gender'])

# values() 获取所有的 values 值
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
print(dict1.values())  # dict_values(['Tom', 20, '男'])

# items() 获取字典所有的键值对
dict1 = {'name': 'Tom', 'age': 20, 'gender': '男'}
# dict_items([('name','Tom'), ('age', 20), ('gender', '男')])
print(dict1.items())
