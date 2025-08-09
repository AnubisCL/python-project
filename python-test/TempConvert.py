#TempConvert.py
TempStr = input("请输入带有符号的温度值：")
#[-1]表示倒数第一个字符,[1:3]表示第一，第二但不到第三个
#in是否存在
if TempStr[-1] in ['F','f']:
    #eval()去掉参数最外侧引号并执行余下语句的函数
    #[0:-1]表示从0到倒数第一个,但不包括倒数第一个
    C = (eval(TempStr[0:-1]) - 32)/1.8
    #{:.2f}表示取小数点后两位
    print("转换后的温度是：{:.2f}C".format(C))
elif TempStr[-1] in ['C','c']:
    F = 1.8*eval(TempStr[0:-1])+32
    print("转换后的温度是：{:.2f}F".format(F))
else:
    print("输入格式错误！")
