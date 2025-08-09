#PythonDraw.py
import turtle       #form...import,import...as...
turtle.setup(650, 350, 200, 200)    #窗体大小及位置
turtle.penup()      #抬笔
turtle.fd(-250)     #海龟后退250个像素
turtle.pendown()    #落笔
turtle.pensize(25)  #笔宽
turtle.pencolor("#81ecec")   #颜色(0.63, 0.13, 0.94)或((0.63, 0.13, 0.94))
turtle.seth(-40)    #海龟方向改为 -40度
for i in range(4):  #range(N):产生0到N-1的整数序列/(M,N)M到N-1
    turtle.circle(40, 80)   #画圆(半径,角度)
    turtle.circle(-40, 80)
turtle.circle(40, 80/2)
turtle.fd(40)       #向前(40)像素
turtle.circle(16, 180)
turtle.fd(40 * 2/3)
turtle.done()       #程序结束后需手动关闭窗口，否则自动关闭窗口
