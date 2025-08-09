#TextProBarV3.py
import time
scale = 50
print("执行开始".right(scale//2,"-"))
start = time.perf_counter()
for i in range(scale+1):
    a = '*' * i 
    b = '.' * (scale - i) 
    c = (i/scale)*100
    dur = time.perf_counter() - start
    # ^3 表示占3位 .0f 表示保留小数位 : 不控制格式可省略
    print("\r{:^3.0f}% [{}->{:}] {:.2f}s".format(c,a,b,dur),end="")
    time.sleep(0.1)
print("\n"+"执行结束".center(scale//2,"-"))
