# 学员管理系统
'''
需求：进入系统显示系统功能界面，功能如下：
1、添加学员
2、删除学员
3、修改学员信息
4、查询学员信息
5、显示所有学员信息
6、退出系统
系统共6个功能，用户根据自己需求选取。
'''

# 全局变量
info = []   #存储所有学员信息


# 1. 显示功能界面
def print_info():
    print('-' * 20)
    print('欢迎登录学员管理系统')
    print('1: 添加学员')
    print('2: 删除学员')
    print('3: 修改学员信息')
    print('4: 查询学员信息')
    print('5: 显示所有学员信息')
    print('6: 退出系统')
    print('-' * 20)

# 1、添加学员
def add_info():
    """ 添加学员 """
    """
    需求分析
    1. 接收用户输入学员信息，并保存
    2. 判断是否添加学员信息
        2.1 如果学员姓名已经存在，则报错提示
        2.2 如果学员姓名不存在，则准备空字典，
        将用户输入的数据追加到字典，再列表追加字典数据
    3. 对应的if条件成立的位置调用该函数
    """
    # 接收用户输入学员信息
    new_id = input('请输入学号：')
    new_name = input('请输入姓名：')
    new_tel = input('请输入手机号：')
    # 声明info是全局变量
    global info
    # 检测用户输入的姓名是否存在，存在则报错提示
    for i in info:
        if new_name == i['name']:
            print('该用户已经存在！')
            return
    # 如果用户输入的姓名不存在，则添加该学员信息
    info_dict = {}

    # 将用户输入的数据追加到字典
    info_dict['id'] = new_id
    info_dict['name'] = new_name
    info_dict['tel'] = new_tel

    # 将这个学员的字典数据追加到列表
    info.append(info_dict)

    print(info)


# 2.删除学员
def del_info():
    """删除学员"""
    """
    需求分析: 按用户输入的学员姓名进行删除
    1. 用户输入目标学员姓名
    2. 检查这个学员是否存在
        2.1 如果存在，则列表删除这个数据
        2.2 如果不存在，则提示“该用户不存在”
    3. 对应的if条件成立的位置调用该函数
    """
    # 1. 用户输入要删除的学员的姓名
    del_name = input('请输入要删除的学员的姓名：')
    global info
    # 2. 判断学员是否存在:如果输入的姓名存在则删除，否则报错提示
    for i in info:
        if del_name == i['name']:
            info.remove(i)
            break
    else:
        print('该学员不存在')
    print(info)


# 3.修改函数
def modify_info():
    """修改函数"""
    """
    需求分析
    1. 用户输入目标学员姓名
    2. 检查这个学员是否存在
        2.1 如果存在，则修改这位学员的信息，例如手机号
        2.2 如果不存在，则报错
    3. 对应的if条件成立的位置调用该函数
    """
    # 1. 用户输入要修改的学员的姓名
    modify_name = input('请输入要修改的学员的姓名：')
    global info
    # 2. 判断学员是否存在：如果输入的姓名存在则修改手机号，否则报错提示
    for i in info:
        if modify_name == i['name']:
            i['tel'] = input('请输入新的手机号：')
            break
    else:
        print('该学员不存在')

    print(info)


# 4.查询学员
def search_info():
    """查询学员"""
    # 1. 输入要查找的学员姓名：
    search_name = input('请输入要查找的学员姓名：')
    global info
    # 2. 判断学员是否存在：如果输入的姓名存在则显示这位学员信息，否则报错提示
    for i in info:
        if search_name == i['name']:
            print('查找到的学员信息如下：----------')
            print(f"该学员的学号是{i['id']}, 姓名是{i['name']}, 手机号是{i['tel']}")
        break
    else:
        print('该学员不存在')


# 5.显示所有学员信息
def print_all():
    """ 显示所有学员信息 """
    print('学号\t姓名\t手机号')
    for i in info:
        print(f'{i["id"]}\t{i["name"]}\t{i["tel"]}')


while True:
    # 1. 显示功能界面
    print_info()

    # 2. 用户选择功能
    user_num = input('请选择您需要的功能序号：')
    # 3. 根据用户选择，执行不同的功能
    if user_num == '1':
        # print('添加学员')
        add_info()
    elif user_num == '2':
        # print('删除学员')
        del_info()
    elif user_num == '3':
        # print('修改学员信息')
        modify_info()
    elif user_num == '4':
        # print('查询学员信息')
        search_info()
    elif user_num == '5':
        # print('显示所有学员信息')
        print_all()
    elif user_num == '6':
        # print('退出系统')
        exit_flag = input('确定要退出吗？(yes/no):')
        if exit_flag == 'yes':
            break
    else:
        user_num = input('输入错误，请重新输入:')
