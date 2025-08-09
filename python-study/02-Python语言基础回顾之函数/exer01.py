'''
需求：用户到ATM机取钱：
1. 输入密码后显示"选择功能"界面
2. 查询余额后显示"选择功能"界面
3. 取2000钱后显示"选择功能"界面
特点：显示“选择功能”界面需要重复输出给用户，怎么实现？

函数就是将一段具有独立功能的代码块 整合到一个整体并命名，
在需要的位置调用这个名称即可完成对应的需求。
函数在开发过程中，可以更高效的实现代码重用。
'''
def select_func():
    flag = True
    while flag:
        print('-----请选择功能-----')
        print('查询余额-0')
        print('存款-1')
        print('取款-2')
        selection = input('您的选择是：')
        print('-----请选择功能-----')
        if selection[0] not in {'0','1','2'} :
            print('#选择错误，请重新输入。#')
        else:
            return selection[0]

def use_func():
    while True:
        if selection == '0':
            print('查询余额完毕')
            # 显示"选择功能"界面
            selection = select_func()
        elif selection == '1':
            print('存了2000元钱')
            # 显示"选择功能"界面
            selection = select_func()
        elif selection == '2':
            print('取了2000元钱')
            # 显示"选择功能"界面
            selection = select_func()
        else:
            print('#选择错误，请重新输入。#')
            break


password = '123'
passvalue = input('登录请输入密码：')
while True:
    if passvalue == password:
        print('密码正确登录成功')
        # 显示"选择功能"界面
        selection = select_func()
    else:
        print('密码不正确登录失败')
        passvalue = input('请重新输入:')


